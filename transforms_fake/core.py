import os
import random
import cv2
import numpy as np
from typing import Optional, Tuple, List, Callable
from .utils import rotate_image_and_mask, find_background_patch


class ImageTransformer:
    """
    Classe principal para transformação de imagens com rotação e posicionamento aleatório.
    
    Esta classe permite processar imagens contendo objetos segmentados por máscaras,
    criando variações com rotações aleatórias e posicionamento em fundos limpos.
    """
    
    def __init__(self, target_size: Tuple[int, int] = (1428, 1068)):
        """
        Inicializa o transformador de imagens.
        
        Args:
            target_size: Tupla (largura, altura) para redimensionar as imagens
        """
        self.target_size = target_size
        
    def process_images(self, 
                      image_dir: str,
                      mask_dir: str,
                      output_dir: str,
                      num_backgrounds: int = 5,
                      num_variations_per_background: int = 10,
                      rotation_range: Tuple[float, float] = (-180, 180),
                      mask_classes: List[int] = [1, 2, 3],
                      log_callback: Optional[Callable[[str], None]] = None) -> dict:
        """
        Processa as imagens criando variações com rotações e posicionamentos aleatórios.
        
        Args:
            image_dir: Diretório contendo as imagens originais
            mask_dir: Diretório contendo as máscaras correspondentes
            output_dir: Diretório base para salvar os resultados
            num_backgrounds: Número de imagens a usar como base
            num_variations_per_background: Número de variações por imagem base
            rotation_range: Tupla (min, max) para ângulos de rotação em graus
            mask_classes: Lista de valores de classe na máscara que representam o objeto
            log_callback: Função opcional para logging
            
        Returns:
            dict: Estatísticas do processamento
        """
        # Criar diretórios de saída
        output_backgrounds_dir = os.path.join(output_dir, 'fundos_sem_objeto')
        output_variations_dir = os.path.join(output_dir, 'variações')
        output_masks_dir = os.path.join(output_dir, 'máscaras')
        
        for dir_path in [output_backgrounds_dir, output_variations_dir, output_masks_dir]:
            os.makedirs(dir_path, exist_ok=True)
        
        def log(text: str):
            if log_callback:
                log_callback(text)
            else:
                print(text)
        
        # Listar arquivos de imagem
        image_files = sorted([f for f in os.listdir(image_dir) 
                            if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
        
        log(f'🔎 Encontradas {len(image_files)} imagens para processar.')
        
        processed_count = 0
        error_count = 0
        total_variations = 0
        
        selected_backgrounds = image_files[:num_backgrounds]
        
        for img_index, img_file in enumerate(selected_backgrounds):
            try:
                result = self._process_single_image(
                    img_file, image_dir, mask_dir,
                    output_backgrounds_dir, output_variations_dir, output_masks_dir,
                    num_variations_per_background, rotation_range, mask_classes, log
                )
                
                if result['success']:
                    processed_count += 1
                    total_variations += result['variations_created']
                    log(f'✅ Processado {img_file} - {result["variations_created"]} variações criadas.')
                else:
                    error_count += 1
                    log(f'⚠️ Erro ao processar {img_file}: {result["error"]}')
                    
            except Exception as e:
                error_count += 1
                log(f'❌ Erro inesperado ao processar {img_file}: {str(e)}')
        
        stats = {
            'total_images_found': len(image_files),
            'images_processed': processed_count,
            'images_with_errors': error_count,
            'total_variations_created': total_variations
        }
        
        log(f'\n📊 Processamento concluído:')
        log(f'   - Imagens encontradas: {stats["total_images_found"]}')
        log(f'   - Imagens processadas: {stats["images_processed"]}')
        log(f'   - Imagens com erro: {stats["images_with_errors"]}')
        log(f'   - Total de variações criadas: {stats["total_variations_created"]}')
        
        return stats
    
    def _process_single_image(self, img_file: str, image_dir: str, mask_dir: str,
                            output_backgrounds_dir: str, output_variations_dir: str,
                            output_masks_dir: str, num_variations: int,
                            rotation_range: Tuple[float, float], mask_classes: List[int],
                            log_func: Callable[[str], None]) -> dict:
        """Processa uma única imagem e suas variações."""
        
        # Encontrar máscara correspondente
        mask_file = self._get_matching_mask(img_file, mask_dir)
        if mask_file is None:
            return {'success': False, 'error': 'Máscara não encontrada'}
        
        # Carregar imagem e máscara
        img_path = os.path.join(image_dir, img_file)
        mask_path = os.path.join(mask_dir, mask_file)
        
        img = cv2.imread(img_path)
        mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
        
        if img is None or mask is None:
            return {'success': False, 'error': 'Erro ao carregar imagem ou máscara'}
        
        # Redimensionar
        img = cv2.resize(img, self.target_size)
        mask = cv2.resize(mask, self.target_size, interpolation=cv2.INTER_NEAREST)
        
        # Criar máscara binária para o objeto
        object_mask = np.isin(mask, mask_classes).astype(np.uint8) * 255
        object_mask_inv = cv2.bitwise_not(object_mask)
        
        # Encontrar coordenadas do objeto
        coords = cv2.findNonZero(object_mask)
        if coords is None:
            return {'success': False, 'error': 'Nenhum objeto encontrado na máscara'}
        
        x, y, w, h = cv2.boundingRect(coords)
        log_func(f'Processando {img_file}, objeto bbox: x={x}, y={y}, w={w}, h={h}')
        
        # Extrair objeto e máscara
        object_cropped = img[y:y+h, x:x+w]
        object_mask_cropped = object_mask[y:y+h, x:x+w]
        object_mask_original_cropped = mask[y:y+h, x:x+w]
        
        # Criar fundo sem objeto
        background_clean = self._create_clean_background(img, mask, object_mask_inv, 
                                                       (x, y, w, h))
        if background_clean is None:
            return {'success': False, 'error': 'Não foi possível criar fundo limpo'}
        
        # Salvar fundo limpo
        base_name = os.path.splitext(img_file)[0]
        background_path = os.path.join(output_backgrounds_dir, f'fundo_limpo_{img_file}')
        cv2.imwrite(background_path, background_clean)
        
        # Salvar máscara do fundo (toda zero)
        background_mask = np.zeros_like(mask, dtype=np.uint8)
        background_mask_path = os.path.join(output_masks_dir, f'fundo_limpo_mask_{img_file}')
        cv2.imwrite(background_mask_path, background_mask)
        
        # Criar variações
        variations_created = 0
        for i in range(num_variations):
            try:
                variation_img, variation_mask = self._create_variation(
                    background_clean, object_cropped, object_mask_original_cropped,
                    rotation_range, mask
                )
                
                # Salvar variação
                variation_path = os.path.join(output_variations_dir, f'{base_name}_var{i+1}.png')
                mask_path = os.path.join(output_masks_dir, f'{base_name}_var{i+1}_mask.png')
                
                cv2.imwrite(variation_path, variation_img)
                cv2.imwrite(mask_path, variation_mask)
                variations_created += 1
                
            except Exception as e:
                log_func(f'⚠️ Erro ao criar variação {i+1}: {str(e)}')
        
        return {'success': True, 'variations_created': variations_created}
    
    def _get_matching_mask(self, img_filename: str, mask_dir: str) -> Optional[str]:
        """Encontra a máscara correspondente a uma imagem."""
        base_name = os.path.splitext(img_filename)[0]
        for f in os.listdir(mask_dir):
            if os.path.splitext(f)[0] == base_name:
                return f
        return None
    
    def _create_clean_background(self, img: np.ndarray, mask: np.ndarray, 
                               object_mask_inv: np.ndarray, 
                               object_rect: Tuple[int, int, int, int]) -> Optional[np.ndarray]:
        """Cria um fundo limpo substituindo a área do objeto por uma região de fundo."""
        x, y, w, h = object_rect
        
        # Criar fundo inicial sem objeto
        background = cv2.bitwise_and(img, img, mask=object_mask_inv)
        
        # Encontrar patch de fundo para substituir a área do objeto
        patch_pos = find_background_patch(mask, w, h, object_rect)
        if patch_pos is None:
            return None
        
        patch_x, patch_y = patch_pos
        patch = img[patch_y:patch_y+h, patch_x:patch_x+w]
        background[y:y+h, x:x+w] = patch
        
        return background
    
    def _create_variation(self, background: np.ndarray, object_img: np.ndarray,
                         object_mask: np.ndarray, rotation_range: Tuple[float, float],
                         original_mask: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Cria uma variação com objeto rotacionado em posição aleatória."""
        
        # Rotacionar objeto
        angle = random.uniform(rotation_range[0], rotation_range[1])
        rotated_object, rotated_mask = rotate_image_and_mask(object_img, object_mask, angle)
        
        # Preparar imagem e máscara de saída
        variation_img = background.copy()
        variation_mask = np.zeros_like(original_mask, dtype=np.uint8)
        
        # Dimensões do objeto rotacionado
        h_r, w_r = rotated_object.shape[:2]
        
        # Escolher posição aleatória
        max_x = self.target_size[0] - w_r
        max_y = self.target_size[1] - h_r
        
        if max_x <= 0 or max_y <= 0:
            # Se o objeto rotacionado é maior que a imagem, usar posição central
            x_new = max(0, (self.target_size[0] - w_r) // 2)
            y_new = max(0, (self.target_size[1] - h_r) // 2)
        else:
            x_new = random.randint(0, max_x)
            y_new = random.randint(0, max_y)
        
        # Aplicar objeto rotacionado na nova posição
        roi = variation_img[y_new:y_new+h_r, x_new:x_new+w_r]
        mask_bin = (rotated_mask > 0).astype(np.uint8) * 255
        mask_inv = cv2.bitwise_not(mask_bin)
        
        roi_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
        object_fg = cv2.bitwise_and(rotated_object, rotated_object, mask=mask_bin)
        dst = cv2.add(roi_bg, object_fg)
        
        variation_img[y_new:y_new+h_r, x_new:x_new+w_r] = dst
        variation_mask[y_new:y_new+h_r, x_new:x_new+w_r] = rotated_mask
        
        return variation_img, variation_mask