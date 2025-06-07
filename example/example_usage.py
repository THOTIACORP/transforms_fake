#!/usr/bin/env python3
"""
Exemplo de uso da biblioteca transforms_fake
"""

import os
import sys
from transforms_fake import ImageTransformer
from transforms_fake.utils import validate_inputs


def exemplo_basico():
    """Exemplo básico de uso da biblioteca."""
    print("🚀 Exemplo básico - Transforms Fake")
    print("-" * 50)
    
    # Configurar caminhos (ajuste conforme sua estrutura)
    image_dir = "dados/imagens"
    mask_dir = "dados/mascaras"  
    output_dir = "dados/saida"
    
    # Validar entradas primeiro
    validation = validate_inputs(image_dir, mask_dir, output_dir)
    
    if not validation['valid']:
        print("❌ Erro de validação:")
        for error in validation['errors']:
            print(f"   - {error}")
        return False
    
    if validation['warnings']:
        print("⚠️ Avisos:")
        for warning in validation['warnings']:
            print(f"   - {warning}")
    
    print(f"✅ Validação passou! Encontradas {validation['image_count']} imagens")
    
    # Criar transformador
    transformer = ImageTransformer(target_size=(1024, 768))
    
    # Função de callback para logging
    def log_progress(message):
        print(f"[PROGRESS] {message}")
    
    # Processar imagens
    print("\n🔄 Iniciando processamento...")
    
    try:
        stats = transformer.process_images(
            image_dir=image_dir,
            mask_dir=mask_dir,
            output_dir=output_dir,
            num_backgrounds=3,              # Usar 3 imagens como base
            num_variations_per_background=5, # 5 variações por imagem
            rotation_range=(-90, 90),       # Rotação entre -90° e +90°
            mask_classes=[1, 2, 3],         # Classes que representam o objeto
            log_callback=log_progress
        )
        
        print("\n🎉 Processamento concluído com sucesso!")
        print("📊 Estatísticas finais:")
        print(f"   - Imagens encontradas: {stats['total_images_found']}")
        print(f"   - Imagens processadas: {stats['images_processed']}")
        print(f"   - Imagens com erro: {stats['images_with_errors']}")
        print(f"   - Total de variações criadas: {stats['total_variations_created']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro durante processamento: {e}")
        return False


def exemplo_avancado():
    """Exemplo avançado com configurações customizadas."""
    print("\n🎛️ Exemplo avançado - Configurações customizadas")
    print("-" * 60)
    
    # Configuração mais específica
    transformer = ImageTransformer(target_size=(1428, 1068))
    
    # Parâmetros customizados
    config = {
        'image_dir': "dados/ratos",
        'mask_dir': "dados/masks",
        'output_dir': "dados/resultado_avancado",
        'num_backgrounds': 10,
        'num_variations_per_background': 20,
        'rotation_range': (-180, 180),  # Rotação completa
        'mask_classes': [1, 2, 3, 4],   # Incluir mais classes
    }
    
    # Log mais detalhado
    log_count = 0
    def detailed_log(message):
        nonlocal log_count
        log_count += 1
        print(f"[{log_count:03d}] {message}")
    
    print(f"🔧 Configuração:")
    for key, value in config.items():
        if key != 'log_callback':
            print(f"   - {key}: {value}")
    
    try:
        stats = transformer.process_images(
            **config,
            log_callback=detailed_log
        )
        
        print(f"\n✨ Processamento avançado concluído!")
        print(f"📈 Taxa de sucesso: {stats['images_processed']}/{stats['total_images_found']} imagens")
        
        # Calcular médias
        if stats['images_processed'] > 0:
            avg_variations = stats['total_variations_created'] / stats['images_processed']
            print(f"📊 Média de variações por imagem: {avg_variations:.1f}")
        
        return stats
        
    except Exception as e:
        print(f"❌ Erro no processamento avançado: {e}")
        return None


def exemplo_com_filtros():
    """Exemplo usando apenas algumas imagens específicas."""
    print("\n🎯 Exemplo com filtros - Processamento seletivo")
    print("-" * 55)
    
    # Listar imagens disponíveis primeiro
    image_dir = "dados/imagens"
    
    if not os.path.exists(image_dir):
        print(f"❌ Diretório {image_dir} não encontrado")
        return
    
    image_files = [f for f in os.listdir(image_dir) 
                   if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    print(f"📋 Imagens disponíveis ({len(image_files)}):")
    for i, img in enumerate(image_files[:10]):  # Mostrar apenas as primeiras 10
        print(f"   {i+1:2d}. {img}")
    
    if len(image_files) > 10:
        print(f"   ... e mais {len(image_files) - 10} imagens")
    
    # Processar apenas as primeiras 2 imagens com muitas variações
    transformer = ImageTransformer()
    
    stats = transformer.process_images(
        image_dir=image_dir,
        mask_dir="dados/mascaras",
        output_dir="dados/saida_filtrada",
        num_backgrounds=2,     # Apenas 2 imagens
        num_variations_per_background=15,  # Muitas variações
        rotation_range=(-45, 45),  # Rotação moderada
        mask_classes=[1, 2, 3],
        log_callback=lambda msg: print(f"[FILTER] {msg}")
    )
    
    print(f"\n🎯 Processamento seletivo concluído!")
    return stats


def main():
    """Função principal - executa todos os exemplos."""
    print("🌟 Demonstração da biblioteca transforms_fake")
    print("=" * 50)
    
    # Verificar se os diretórios básicos existem
    required_dirs = ["dados/imagens", "dados/mascaras"]
    missing_dirs = [d for d in required_dirs if not os.path.exists(d)]
    
    if missing_dirs:
        print("❌ Diretórios necessários não encontrados:")
        for d in missing_dirs:
            print(f"   - {d}")
        print("\n💡 Dica: Crie os diretórios e adicione suas imagens e máscaras")
        print("Estrutura esperada:")
        print("dados/")
        print("├── imagens/")
        print("│   ├── img001.jpg")
        print("│   └── img002.jpg")
        print("└── mascaras/")
        print("    ├── img001.png")
        print("    └── img002.png")
        return
    
    # Executar exemplos
    try:
        # Exemplo 1: Básico
        success = exemplo_basico()
        
        if success:
            # Exemplo 2: Avançado
            exemplo_avancado()
            
            # Exemplo 3: Com filtros
            exemplo_com_filtros()
            
            print("\n🎉 Todos os exemplos foram executados com sucesso!")
            print("📁 Verifique os diretórios de saída para ver os resultados")
        else:
            print("\n⚠️ Exemplo básico falhou. Verifique a configuração.")
            
    except KeyboardInterrupt:
        print("\n⏹️ Execução interrompida pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()