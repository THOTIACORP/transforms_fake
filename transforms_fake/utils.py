import random
import cv2
import numpy as np
from typing import Optional, Tuple


def rotate_image_and_mask(image: np.ndarray, mask: np.ndarray, angle: float) -> Tuple[np.ndarray, np.ndarray]:
    """
    Rotaciona uma imagem e sua máscara mantendo o mesmo tamanho.
    
    Args:
        image: Imagem a ser rotacionada
        mask: Máscara correspondente à imagem
        angle: Ângulo de rotação em graus
        
    Returns:
        Tupla contendo (imagem_rotacionada, máscara_rotacionada)
    """
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    
    # Matriz de rotação
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    
    # Rotacionar imagem
    rotated_img = cv2.warpAffine(
        image, M, (w, h), 
        flags=cv2.INTER_LINEAR, 
        borderMode=cv2.BORDER_CONSTANT, 
        borderValue=(0, 0, 0)
    )
    
    # Rotacionar máscara
    rotated_mask = cv2.warpAffine(
        mask, M, (w, h), 
        flags=cv2.INTER_NEAREST, 
        borderMode=cv2.BORDER_CONSTANT, 
        borderValue=0
    )
    
    return rotated_img, rotated_mask


def find_background_patch(mask: np.ndarray, w: int, h: int, 
                         exclude_rect: Tuple[int, int, int, int],
                         max_attempts: int = 1000) -> Optional[Tuple[int, int]]:
    """
    Encontra uma região de fundo (pixels com valor 0) que não se sobrepõe a uma área excluída.
    
    Args:
        mask: Máscara onde 0 representa fundo
        w: Largura da região desejada
        h: Altura da região desejada
        exclude_rect: Tupla (x, y, width, height) da região a excluir
        max_attempts: Número máximo de tentativas para encontrar uma região válida
        
    Returns:
        Tupla (x, y) da posição encontrada, ou None se não encontrou
    """
    height, width = mask.shape
    ex, ey, ew, eh = exclude_rect
    
    for attempt in range(max_attempts):
        # Posição aleatória
        x = random.randint(0, width - w)
        y = random.randint(0, height - h)
        
        # Verificar se se sobrepõe à região excluída
        if (x < ex + ew and x + w > ex and y < ey + eh and y + h > ey):
            continue
        
        # Verificar se a região é toda de fundo (valor 0)
        patch = mask[y:y+h, x:x+w]
        if np.all(patch == 0):
            return (x, y)
    
    return None


def get_object_bbox(mask: np.ndarray, object_classes: list = [1, 2, 3]) -> Optional[Tuple[int, int, int, int]]:
    """
    Encontra a bounding box do objeto na máscara.
    
    Args:
        mask: Máscara de segmentação
        object_classes: Lista de valores de classe que representam o objeto
        
    Returns:
        Tupla (x, y, width, height) ou None se não encontrou objeto
    """
    # Criar máscara binária para o objeto
    object_mask = np.isin(mask, object_classes).astype(np.uint8) * 255
    
    # Encontrar coordenadas do objeto
    coords = cv2.findNonZero(object_mask)
    if coords is None:
        return None
    
    return cv2.boundingRect(coords)


def validate_inputs(image_dir: str, mask_dir: str, output_dir: str) -> dict:
    """
    Valida os diretórios de entrada e saída.
    
    Args:
        image_dir: Diretório de imagens
        mask_dir: Diretório de máscaras
        output_dir: Diretório de saída
        
    Returns:
        dict com informações de validação
    """
    import os
    
    validation = {
        'valid': True,
        'errors': [],
        'warnings': []
    }
    
    # Verificar se diretórios existem
    if not os.path.exists(image_dir):
        validation['valid'] = False
        validation['errors'].append(f"Diretório de imagens não existe: {image_dir}")
    
    if not os.path.exists(mask_dir):
        validation['valid'] = False
        validation['errors'].append(f"Diretório de máscaras não existe: {mask_dir}")
    
    # Verificar se diretório de saída pode ser criado
    try:
        os.makedirs(output_dir, exist_ok=True)
    except Exception as e:
        validation['valid'] = False
        validation['errors'].append(f"Não foi possível criar diretório de saída: {e}")
    
    # Contar arquivos
    if validation['valid']:
        image_extensions = ('.png', '.jpg', '.jpeg')
        image_files = [f for f in os.listdir(image_dir) 
                      if f.lower().endswith(image_extensions)]
        mask_files = [f for f in os.listdir(mask_dir) 
                     if f.lower().endswith(image_extensions)]
        
        validation['image_count'] = len(image_files)
        validation['mask_count'] = len(mask_files)
        
        if len(image_files) == 0:
            validation['valid'] = False
            validation['errors'].append("Nenhuma imagem encontrada no diretório de imagens")
        
        if len(mask_files) == 0:
            validation['valid'] = False
            validation['errors'].append("Nenhuma máscara encontrada no diretório de máscaras")
        
        if len(image_files) != len(mask_files):
            validation['warnings'].append(
                f"Número de imagens ({len(image_files)}) diferente do número de máscaras ({len(mask_files)})"
            )
    
    return validation


def create_preview_grid(images: list, max_images: int = 9, 
                       grid_size: Tuple[int, int] = (3, 3)) -> Optional[np.ndarray]:
    """
    Cria uma grade de preview das imagens processadas.
    
    Args:
        images: Lista de imagens (arrays numpy)
        max_images: Número máximo de imagens na grade
        grid_size: Tupla (linhas, colunas) da grade
        
    Returns:
        Imagem da grade ou None se não há imagens
    """
    if not images:
        return None
    
    # Selecionar imagens para a grade
    selected_images = images[:min(max_images, len(images))]
    rows, cols = grid_size
    
    # Redimensionar imagens para tamanho uniforme
    thumb_size = (200, 150)
    thumbnails = []
    
    for img in selected_images:
        if len(img.shape) == 3:
            thumb = cv2.resize(img, thumb_size)
        else:
            thumb = cv2.resize(img, thumb_size)
            thumb = cv2.cvtColor(thumb, cv2.COLOR_GRAY2BGR)
        thumbnails.append(thumb)
    
    # Preencher com imagens em branco se necessário
    while len(thumbnails) < rows * cols:
        blank = np.zeros((thumb_size[1], thumb_size[0], 3), dtype=np.uint8)
        thumbnails.append(blank)
    
    # Criar grade
    grid_rows = []
    for r in range(rows):
        row_images = thumbnails[r * cols:(r + 1) * cols]
        grid_row = np.hstack(row_images)
        grid_rows.append(grid_row)
    
    grid = np.vstack(grid_rows)
    return grid