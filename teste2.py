#!/usr/bin/env python3
"""
Script para usar transforms_fake com dados reais
Processa as imagens nas pastas 'rats' e 'masks'
"""

import os
import sys
from transforms_fake import ImageTransformer

def verificar_dados():
    """Verifica se os dados estão disponíveis e bem estruturados."""
    print("🔍 Verificando dados disponíveis...")
    print("-" * 50)
    
    # Verificar diretórios
    rats_dir = "rats"
    masks_dir = "masks"
    
    if not os.path.exists(rats_dir):
        print(f"❌ Diretório '{rats_dir}' não encontrado!")
        return False
    
    if not os.path.exists(masks_dir):
        print(f"❌ Diretório '{masks_dir}' não encontrado!")
        return False
    
    # Listar arquivos
    rat_files = [f for f in os.listdir(rats_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    mask_files = [f for f in os.listdir(masks_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    print(f"📂 Pasta '{rats_dir}': {len(rat_files)} arquivos encontrados")
    print(f"📂 Pasta '{masks_dir}': {len(mask_files)} arquivos encontrados")
    
    if len(rat_files) == 0:
        print("❌ Nenhuma imagem encontrada na pasta 'rats'!")
        return False
    
    if len(mask_files) == 0:
        print("❌ Nenhuma máscara encontrada na pasta 'masks'!")
        return False
    
    # Mostrar alguns exemplos
    print(f"\n📄 Exemplos de arquivos:")
    print(f"   Ratos: {rat_files[:3]}...")
    print(f"   Máscaras: {mask_files[:3]}...")
    
    # Verificar correspondência de nomes
    rat_names = set(os.path.splitext(f)[0] for f in rat_files)
    mask_names = set(os.path.splitext(f)[0] for f in mask_files)
    
    matching = rat_names.intersection(mask_names)
    print(f"\n🔗 Pares correspondentes: {len(matching)}")
    
    if len(matching) == 0:
        print("⚠️ AVISO: Nenhum arquivo com nome correspondente encontrado!")
        print("   Exemplo: 'rats/frame_001.jpg' deve ter 'masks/frame_001.png'")
    else:
        print(f"✅ Exemplos de pares: {list(matching)[:3]}")
    
    return len(matching) > 0

def processar_basico():
    """Processamento básico com configurações padrão."""
    print("\n🚀 Processamento Básico")
    print("-" * 50)
    
    # Criar transformador
    transformer = ImageTransformer(target_size=(1428, 1068))
    
    # Configurações básicas
    config = {
        'image_dir': 'rats',
        'mask_dir': 'masks',
        'output_dir': 'resultado_basico',
        'num_backgrounds': 3,              # Usar 3 imagens como base
        'num_variations_per_background': 5, # 5 variações por imagem
        'rotation_range': (-180, 180),     # Rotação completa
        'mask_classes': [1, 2, 3]          # Classes da máscara que representam ratos
    }
    
    print("⚙️ Configurações:")
    for key, value in config.items():
        print(f"   {key}: {value}")
    
    def log_progresso(mensagem):
        print(f"[LOG] {mensagem}")
    
    try:
        print("\n🔄 Iniciando processamento...")
        stats = transformer.process_images(
            **config,
            log_callback=log_progresso
        )
        
        print("\n✅ Processamento concluído!")
        print("📊 Resultados:")
        for key, value in stats.items():
            print(f"   {key}: {value}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro durante processamento: {e}")
        import traceback
        traceback.print_exc()
        return False

def processar_customizado():
    """Processamento com configurações customizadas."""
    print("\n🎛️ Processamento Customizado")
    print("-" * 50)
    
    # Perguntar configurações ao usuário
    print("📋 Configure o processamento:")
    
    try:
        num_backgrounds = int(input("Quantas imagens usar como base? (padrão: 5): ") or "5")
        num_variations = int(input("Quantas variações por imagem? (padrão: 10): ") or "10")
        
        print("Intervalo de rotação:")
        rot_min = float(input("  Ângulo mínimo (padrão: -180): ") or "-180")
        rot_max = float(input("  Ângulo máximo (padrão: 180): ") or "180")
        
        mask_classes_input = input("Classes da máscara (padrão: 1,2,3): ") or "1,2,3"
        mask_classes = [int(x.strip()) for x in mask_classes_input.split(',')]
        
        output_dir = input("Diretório de saída (padrão: resultado_customizado): ") or "resultado_customizado"
        
    except (ValueError, KeyboardInterrupt):
        print("❌ Entrada inválida ou cancelada pelo usuário")
        return False
    
    # Criar transformador
    transformer = ImageTransformer(target_size=(1428, 1068))
    
    # Configuração customizada
    config = {
        'image_dir': 'rats',
        'mask_dir': 'masks',
        'output_dir': output_dir,
        'num_backgrounds': num_backgrounds,
        'num_variations_per_background': num_variations,
        'rotation_range': (rot_min, rot_max),
        'mask_classes': mask_classes
    }
    
    print("\n⚙️ Configuração final:")
    for key, value in config.items():
        print(f"   {key}: {value}")
    
    confirmacao = input("\nProsseguir? (s/N): ").strip().lower()
    if confirmacao not in ['s', 'sim', 'y', 'yes']:
        print("⏹️ Cancelado pelo usuário")
        return False
    
    def log_progresso(mensagem):
        print(f"[LOG] {mensagem}")
    
    try:
        print("\n🔄 Iniciando processamento customizado...")
        stats = transformer.process_images(
            **config,
            log_callback=log_progresso
        )
        
        print("\n✅ Processamento customizado concluído!")
        print("📊 Resultados:")
        for key, value in stats.items():
            print(f"   {key}: {value}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro durante processamento: {e}")
        import traceback
        traceback.print_exc()
        return False

def processar_rapido():
    """Processamento rápido para teste."""
    print("\n⚡ Processamento Rápido (Teste)")
    print("-" * 50)
    
    transformer = ImageTransformer(target_size=(800, 600))  # Tamanho menor para rapidez
    
    config = {
        'image_dir': 'rats',
        'mask_dir': 'masks',
        'output_dir': 'teste_rapido',
        'num_backgrounds': 1,              # Apenas 1 imagem
        'num_variations_per_background': 3, # Apenas 3 variações
        'rotation_range': (-45, 45),       # Rotação limitada
        'mask_classes': [1, 2, 3]
    }
    
    print("⚙️ Configuração de teste rápido:")
    for key, value in config.items():
        print(f"   {key}: {value}")
    
    def log_progresso(mensagem):
        print(f"[LOG] {mensagem}")
    
    try:
        print("\n🔄 Executando teste rápido...")
        stats = transformer.process_images(
            **config,
            log_callback=log_progresso
        )
        
        print("\n✅ Teste rápido concluído!")
        print("📊 Resultados:")
        for key, value in stats.items():
            print(f"   {key}: {value}")
        
        # Mostrar arquivos criados
        if os.path.exists(config['output_dir']):
            print(f"\n📁 Arquivos criados em '{config['output_dir']}':")
            for root, dirs, files in os.walk(config['output_dir']):
                for file in files[:10]:  # Mostrar apenas os primeiros 10
                    rel_path = os.path.relpath(os.path.join(root, file), config['output_dir'])
                    print(f"   📄 {rel_path}")
                if len(files) > 10:
                    print(f"   ... e mais {len(files) - 10} arquivos")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro durante teste: {e}")
        import traceback
        traceback.print_exc()
        return False

def processar_com_gui():
    """Abre a interface gráfica."""
    print("\n🖥️ Abrindo Interface Gráfica")
    print("-" * 50)
    
    try:
        from transforms_fake.gui import main
        print("🚀 Iniciando GUI...")
        print("💡 Dica: Configure os diretórios para 'rats' e 'masks'")
        main()
        
    except ImportError as e:
        print(f"❌ Erro ao importar GUI: {e}")
        print("💡 Instale PyQt5: pip install PyQt5")
        return False
    except Exception as e:
        print(f"❌ Erro na GUI: {e}")
        return False

def main():
    """Função principal - menu de opções."""
    print("🐀 Transforms Fake - Processamento de Ratos")
    print("=" * 60)
    
    # Verificar dados primeiro
    if not verificar_dados():
        print("\n❌ Problemas com os dados. Verifique as pastas 'rats' e 'masks'.")
        return
    
    print("\n🎯 Escolha uma opção:")
    print("1. 🚀 Processamento Básico (3 fundos, 5 variações)")
    print("2. ⚡ Teste Rápido (1 fundo, 3 variações)")
    print("3. 🎛️ Processamento Customizado")
    print("4. 🖥️ Interface Gráfica")
    print("5. ❌ Sair")
    
    while True:
        try:
            escolha = input("\nDigite sua escolha (1-5): ").strip()
            
            if escolha == "1":
                processar_basico()
                break
            elif escolha == "2":
                processar_rapido()
                break
            elif escolha == "3":
                processar_customizado()
                break
            elif escolha == "4":
                processar_com_gui()
                break
            elif escolha == "5":
                print("👋 Saindo...")
                break
            else:
                print("❌ Opção inválida. Escolha 1-5.")
                
        except KeyboardInterrupt:
            print("\n👋 Saindo...")
            break
        except Exception as e:
            print(f"❌ Erro: {e}")

if __name__ == "__main__":
    main()