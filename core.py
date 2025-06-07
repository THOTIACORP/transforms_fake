import os
import random
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication

def rotate_image_and_mask(image, mask, angle):
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated_img = cv2.warpAffine(
        image, M, (w, h),
        flags=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=(0,0,0)
    )
    rotated_mask = cv2.warpAffine(
        mask, M, (w, h),
        flags=cv2.INTER_NEAREST,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=0
    )
    return rotated_img, rotated_mask

def process_images(num_fundos, num_ratos_por_fundo, log_widget):
    image_dir = 'rats'
    mask_dir = 'masks'
    output_background_dir = 'ratos/fundos_sem_rato'
    output_ratos_dir = 'ratos/novos_ratos'
    output_masks_dir = 'ratos/mascaras'
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
        for _ in range(1000):
            x = random.randint(0, width - w)
            y = random.randint(0, height - h)
            ex, ey, ew, eh = exclude_rect
            if (x < ex + ew and x + w > ex and y < ey + eh and y + h > ey):
                continue
            patch = mask[y:y+h, x:x+w]
            if np.all(patch == 0):
                return x, y
        return None

    image_files = sorted([
        f for f in os.listdir(image_dir)
        if f.lower().endswith(('.png', '.jpg', '.jpeg'))
    ])
    log(f'🔎 Encontradas {len(image_files)} imagens para processar.')

    fundos = image_files[:num_fundos]
    for idx, img_file in enumerate(fundos, 1):
        mask_file = get_matching_mask(img_file, mask_dir)
        if not mask_file:
            log(f'⚠️ Sem máscara para {img_file}, pulando...')
            continue

        img = cv2.imread(os.path.join(image_dir, img_file))
        mask = cv2.imread(os.path.join(mask_dir, mask_file), cv2.IMREAD_GRAYSCALE)
        if img is None or mask is None:
            log(f'⚠️ Erro ao abrir {img_file} ou sua máscara.')
            continue

        img = cv2.resize(img, target_size)
        mask = cv2.resize(mask, target_size, interpolation=cv2.INTER_NEAREST)

        rat_mask = np.isin(mask, [1,2,3]).astype(np.uint8) * 255
        inv_mask = cv2.bitwise_not(rat_mask)
        coords = cv2.findNonZero(rat_mask)
        if coords is None:
            log(f'⚠️ Sem rato em {img_file}, pulando...')
            continue

        x,y,w,h = cv2.boundingRect(coords)
        log(f'[{idx}/{len(fundos)}] {img_file} – bbox: x={x},y={y},w={w},h={h}')

        cropped = img[y:y+h, x:x+w]
        orig_mask_crop = mask[y:y+h, x:x+w]

        bg = cv2.bitwise_and(img, img, mask=inv_mask)
        patch_pos = find_background_patch(mask, w, h, (x,y,w,h))
        if not patch_pos:
            log(f'⚠️ Sem patch em {img_file}, pulando...')
            continue
        px, py = patch_pos
        bg[ y:y+h, x:x+w ] = img[py:py+h, px:px+w]

        cv2.imwrite(os.path.join(output_background_dir, f'bg_{img_file}'), bg)
        cv2.imwrite(os.path.join(output_masks_dir, f'bg_mask_{img_file}'), np.zeros_like(mask))

        for i in range(num_ratos_por_fundo):
            img_var = bg.copy()
            mask_var = np.zeros_like(mask)
            angle = random.uniform(-180, 180)
            rat_rot, mask_rot = rotate_image_and_mask(cropped, orig_mask_crop, angle)

            h2,w2 = rat_rot.shape[:2]
            nx = random.randint(0, target_size[0]-w2)
            ny = random.randint(0, target_size[1]-h2)

            roi = img_var[ny:ny+h2, nx:nx+w2]
            bin_mask = (mask_rot>0).astype(np.uint8)*255
            bg_roi = cv2.bitwise_and(roi, roi, mask=cv2.bitwise_not(bin_mask))
            fg = cv2.bitwise_and(rat_rot, rat_rot, mask=bin_mask)
            img_var[ny:ny+h2, nx:nx+w2] = cv2.add(bg_roi, fg)
            mask_var[ny:ny+h2, nx:nx+w2] = mask_rot

            cv2.imwrite(os.path.join(output_ratos_dir, f'{os.path.splitext(img_file)[0]}_v{i+1}.png'), img_var)
            cv2.imwrite(os.path.join(output_masks_dir, f'{os.path.splitext(img_file)[0]}_v{i+1}_mask.png'), mask_var)

        log(f'✅ {img_file} — {num_ratos_por_fundo} variações geradas.')
