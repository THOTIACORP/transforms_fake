import os
import random
import cv2
import numpy as np
from PyQt5.QtWidgets import (
    QApplication
)
from transforms_fake import rotate_image_and_mask
def rotate_image_and_mask(image, mask, angle):
    """Rotaciona a imagem e a máscara mantendo o mesmo tamanho."""
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated_img = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0,0,0))
    rotated_mask = cv2.warpAffine(mask, M, (w, h), flags=cv2.INTER_NEAREST, borderMode=cv2.BORDER_CONSTANT, borderValue=0)
    return rotated_img, rotated_mask

def process_images(num_fundos, num_ratos_por_fundo, log_widget):
    image_dir = 'example/rats/image'
    mask_dir = 'example/rats/masks'
    output_background_dir = 'ratos/fundos_sem_rato'
    output_ratos_dir = 'ratos/novos_ratos'
    output_masks_dir = 'ratos/mascaras'  # pasta para máscaras
    os.makedirs(output_background_dir, exist_ok=True)
    os.makedirs(output_ratos_dir, exist_ok=True)
    os.makedirs(output_masks_dir, exist_ok=True)
    target_size = (1428, 1068)

    def log(text):
        log_widget.append(text)
        log_widget.repaint()
        QApplication.processEvents()

    def get_matching_mask(img_filename, mask_dir):
        base_name = os.path.splitext(img_filename)[0]
        for f in os.listdir(mask_dir):
            if os.path.splitext(f)[0] == base_name:
                return f
        return None

    def find_background_patch(mask, w, h, exclude_rect):
        height, width = mask.shape
        for attempt in range(1000):
            x = random.randint(0, width - w)
            y = random.randint(0, height - h)
            ex, ey, ew, eh = exclude_rect
            # Verifica se a região se sobrepõe ao rato, se sim, pula
            if (x < ex + ew and x + w > ex and y < ey + eh and y + h > ey):
                continue
            patch = mask[y:y+h, x:x+w]
            if np.all(patch == 0):
                return x, y
        return None

    image_files = sorted([f for f in os.listdir(image_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
    log(f'🔎 Encontradas {len(image_files)} imagens para processar.')

    fundos_selecionados = image_files[:num_fundos]
    for img_index, img_file in enumerate(fundos_selecionados):
        mask_file = get_matching_mask(img_file, mask_dir)
        if mask_file is None:
            log(f'⚠️ Nenhuma máscara encontrada para {img_file}, pulando...')
            continue

        img_path = os.path.join(image_dir, img_file)
        mask_path = os.path.join(mask_dir, mask_file)

        img = cv2.imread(img_path)
        mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)

        if img is None or mask is None:
            log(f'⚠️ Erro ao abrir imagem ou máscara para {img_file}')
            continue

        img = cv2.resize(img, target_size)
        mask = cv2.resize(mask, target_size, interpolation=cv2.INTER_NEAREST)

        # Mascara binária para rato (qualquer classe 1,2,3 vira 255)
        rato_mask = np.isin(mask, [1, 2, 3]).astype(np.uint8) * 255
        rato_mask_inv = cv2.bitwise_not(rato_mask)

        coords = cv2.findNonZero(rato_mask)
        if coords is None:
            log(f'⚠️ Nenhum rato encontrado na máscara de {img_file}, pulando...')
            continue

        x, y, w, h = cv2.boundingRect(coords)
        log(f'Processando {img_file} ({img_index+1}/{len(fundos_selecionados)}), rato bbox: x={x}, y={y}, w={w}, h={h}')

        rato_cropped = img[y:y+h, x:x+w]
        rato_mask_cropped = rato_mask[y:y+h, x:x+w]
        rato_mask_original_cropped = mask[y:y+h, x:x+w]  # máscara original com classes 1,2,3

        # Cria fundo sem rato
        fundo_sem_rato = cv2.bitwise_and(img, img, mask=rato_mask_inv)

        # Encontra um patch do fundo para substituir a área do rato no fundo_sem_rato
        patch_pos = find_background_patch(mask, w, h, (x, y, w, h))
        if patch_pos is None:
            log(f'⚠️ Não encontrou região de fundo adequada para preencher o rato em {img_file}, pulando...')
            continue

        patch_x, patch_y = patch_pos
        fundo_patch = img[patch_y:patch_y+h, patch_x:patch_x+w]
        fundo_sem_rato[y:y+h, x:x+w] = fundo_patch

        # Salva a imagem do fundo sem rato
        fundo_sem_rato_path = os.path.join(output_background_dir, f'fundo_sem_rato_{img_file}')
        cv2.imwrite(fundo_sem_rato_path, fundo_sem_rato)
        log(f'Fundo sem rato salvo: {fundo_sem_rato_path}')

        # SALVA MÁSCARA TODA ZERO PARA O FUNDO SEM RATO
        fundo_sem_rato_mask = np.zeros_like(mask, dtype=np.uint8)
        fundo_sem_rato_mask_path = os.path.join(output_masks_dir, f'fundo_sem_rato_mask_{img_file}')
        cv2.imwrite(fundo_sem_rato_mask_path, fundo_sem_rato_mask)
        log(f'Máscara do fundo sem rato salva: {fundo_sem_rato_mask_path}')

        max_x = target_size[0] - w
        max_y = target_size[1] - h

        for i in range(num_ratos_por_fundo):
            img_variacao = fundo_sem_rato.copy()
            mask_variacao = np.zeros_like(mask, dtype=np.uint8)

            # Rotação aleatória entre -180 e +180 graus (pode ajustar o range)
            angle = random.uniform(-180, 180)
            rato_rotated, mask_rotated = rotate_image_and_mask(rato_cropped, rato_mask_original_cropped, angle)

            # Ajusta as dimensões após rotação (mesmo tamanho, mas pode ter áreas pretas)
            h_r, w_r = rato_rotated.shape[:2]

            # Escolhe uma posição aleatória onde o rato rotacionado caiba na imagem
            max_x_r = target_size[0] - w_r
            max_y_r = target_size[1] - h_r
            x_new = random.randint(0, max_x_r)
            y_new = random.randint(0, max_y_r)

            roi = img_variacao[y_new:y_new+h_r, x_new:x_new+w_r]
            # Máscara binária para usar no bitwise_and (apenas 255/0)
            mask_rotated_bin = (mask_rotated > 0).astype(np.uint8) * 255
            roi_bg = cv2.bitwise_and(roi, roi, mask=cv2.bitwise_not(mask_rotated_bin))
            rato_fg = cv2.bitwise_and(rato_rotated, rato_rotated, mask=mask_rotated_bin)
            dst = cv2.add(roi_bg, rato_fg)
            img_variacao[y_new:y_new+h_r, x_new:x_new+w_r] = dst

            # Coloca a máscara rotacionada com as classes originais (1,2,3)
            # Usando máscara rotacionada com classes originais, que pode conter valores 1,2,3 em vez de 255
            mask_variacao[y_new:y_new+h_r, x_new:x_new+w_r] = mask_rotated

            output_rato_path = os.path.join(output_ratos_dir, f'{os.path.splitext(img_file)[0]}_var{i+1}.png')
            output_mask_path = os.path.join(output_masks_dir, f'{os.path.splitext(img_file)[0]}_var{i+1}_mask.png')

            cv2.imwrite(output_rato_path, img_variacao)
            cv2.imwrite(output_mask_path, mask_variacao)

        log(f'✅ Processado {img_file} - {num_ratos_por_fundo} variações de rato criadas com máscaras e rotação.')
