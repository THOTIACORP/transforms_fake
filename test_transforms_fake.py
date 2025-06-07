#!/usr/bin/env python3
"""
Exemplos de teste para a biblioteca transforms_fake
Execute cada função separadamente para testar diferentes aspectos
"""

import os
import sys
import numpy as np
import cv2

def test_1_basic_import():
    """Teste 1: Importação básica da biblioteca"""
    print("🧪 Teste 1: Importação Básica")
    print("-" * 40)
    
    try:
        import transforms_fake
        print("✅ Import transforms_fake: OK")
        print(f"📦 Versão: {getattr(transforms_fake, '__version__', 'Não definida')}")
        
        from transforms_fake import ImageTransformer
        print("✅ Import ImageTransformer: OK")
        
        from transforms_fake.utils import rotate_image_and_mask, find_background_patch
        print("✅ Import funções utilitárias: OK")
        
        print("\n🎉 Teste 1: PASSOU")
        return True
        
    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        print("\n💡 Possíveis soluções:")
        print("1. Verifique se executou: pip install -e .")
        print("2. Verifique se está no diretório correto")
        print("3. Verifique se __init__.py existe e tem conteúdo")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

def test_2_class_creation():
    """Teste 2: Criação da classe ImageTransformer"""
    print("\n🧪 Teste 2: Criação da Classe")
    print("-" * 40)
    
    try:
        from transforms_fake import ImageTransformer
        
        # Teste com parâmetros padrão
        transformer1 = ImageTransformer()
        print("✅ Criação com parâmetros padrão: OK")
        print(f"📏 Tamanho padrão: {transformer1.target_size}")
        
        # Teste com parâmetros customizados
        transformer2 = ImageTransformer(target_size=(800, 600))
        print("✅ Criação com parâmetros customizados: OK")
        print(f"📏 Tamanho customizado: {transformer2.target_size}")
        
        print("\n🎉 Teste 2: PASSOU")
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def test_3_utility_functions():
    """Teste 3: Funções utilitárias com dados sintéticos"""
    print("\n🧪 Teste 3: Funções Utilitárias")
    print("-" * 40)
    
    try:
        from transforms_fake.utils import rotate_image_and_mask, find_background_patch
        
        # Criar imagem e máscara sintéticas
        print("📝 Criando dados sintéticos...")
        img = np.zeros((100, 100, 3), dtype=np.uint8)
        img[25:75, 25:75] = [255, 0, 0]  # Quadrado vermelho
        
        mask = np.zeros((100, 100), dtype=np.uint8)
        mask[30:70, 30:70] = 1  # Região do objeto
        
        print("✅ Dados sintéticos criados")
        
        # Teste rotação
        print("🔄 Testando rotação...")
        rotated_img, rotated_mask = rotate_image_and_mask(img, mask, 45)
        
        assert rotated_img.shape == img.shape, "Forma da imagem rotacionada incorreta"
        assert rotated_mask.shape == mask.shape, "Forma da máscara rotacionada incorreta"
        print("✅ Rotação: OK")
        
        # Teste busca de patch de fundo
        print("🔍 Testando busca de patch de fundo...")
        background_mask = np.zeros((200, 200), dtype=np.uint8)
        background_mask[50:150, 50:150] = 1  # Região ocupada
        
        patch_pos = find_background_patch(background_mask, 30, 30, (50, 50, 100, 100))
        
        if patch_pos is not None:
            print(f"✅ Patch encontrado na posição: {patch_pos}")
        else:
            print("⚠️ Nenhum patch encontrado (pode ser normal dependendo da máscara)")
        
        print("\n🎉 Teste 3: PASSOU")
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_4_basic_processing():
    """Teste 4: Processamento básico com dados sintéticos"""
    print("\n🧪 Teste 4: Processamento Básico")
    print("-" * 40)
    
    try:
        from transforms_fake import ImageTransformer
        
        # Criar diretórios temporários
        test_dir = "test_temp"
        img_dir = os.path.join(test_dir, "images")
        mask_dir = os.path.join(test_dir, "masks")
        output_dir = os.path.join(test_dir, "output")
        
        os.makedirs(img_dir, exist_ok=True)
        os.makedirs(mask_dir, exist_ok=True)
        os.makedirs(output_dir, exist_ok=True)
        
        print("📁 Diretórios temporários criados")
        
        # Criar imagem de teste
        test_img = np.zeros((200, 200, 3), dtype=np.uint8)
        test_img[50:150, 50:150] = [0, 255, 0]  # Quadrado verde
        test_img[75:125, 75:125] = [255, 0, 0]  # Quadrado vermelho no centro
        
        # Criar máscara de teste
        test_mask = np.zeros((200, 200), dtype=np.uint8)
        test_mask[75:125, 75:125] = 1  # Objeto na região vermelha
        
        # Salvar arquivos de teste
        cv2.imwrite(os.path.join(img_dir, "test_001.jpg"), test_img)
        cv2.imwrite(os.path.join(mask_dir, "test_001.png"), test_mask)
        
        print("✅ Arquivos de teste criados")
        
        # Testar processamento
        transformer = ImageTransformer(target_size=(200, 200))
        
        def log_callback(msg):
            print(f"[LOG] {msg}")
        
        print("🔄 Executando processamento...")
        stats = transformer.process_images(
            image_dir=img_dir,
            mask_dir=mask_dir,
            output_dir=output_dir,
            num_backgrounds=1,
            num_variations_per_background=2,
            rotation_range=(-45, 45),
            mask_classes=[1],
            log_callback=log_callback
        )
        
        print("📊 Estatísticas do processamento:")
        for key, value in stats.items():
            print(f"   {key}: {value}")
        
        # Limpar arquivos temporários
        import shutil
        shutil.rmtree(test_dir)
        print("🗑️ Arquivos temporários removidos")
        
        print("\n🎉 Teste 4: PASSOU")
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_5_gui_import():
    """Teste 5: Importação da interface gráfica"""
    print("\n🧪 Teste 5: Interface Gráfica")
    print("-" * 40)
    
    try:
        # Testar se PyQt5 está disponível
        try:
            from PyQt5.QtWidgets import QApplication
            print("✅ PyQt5 disponível")
        except ImportError:
            print("❌ PyQt5 não instalado")
            print("💡 Execute: pip install PyQt5")
            return False
        
        # Testar importação da GUI
        from transforms_fake.gui import MainWindow, main
        print("✅ Import da GUI: OK")
        
        # Teste de criação de aplicação (sem mostrar)
        import sys
        app = QApplication(sys.argv if sys.argv else ['test'])
        window = MainWindow()
        print("✅ Criação da janela: OK")
        
        # Não vamos mostrar a janela para não interferir
        app.quit()
        print("✅ Aplicação finalizada")
        
        print("\n🎉 Teste 5: PASSOU")
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_6_with_real_data():
    """Teste 6: Teste com seus dados reais (se disponíveis)"""
    print("\n🧪 Teste 6: Dados Reais")
    print("-" * 40)
    
    try:
        from transforms_fake import ImageTransformer
        
        # Verificar se os diretórios de dados existem
        img_dir = "rats"
        mask_dir = "masks"
        
        if not os.path.exists(img_dir):
            print(f"⚠️ Diretório {img_dir} não encontrado")
            return True  # Não é erro, apenas não há dados
        
        if not os.path.exists(mask_dir):
            print(f"⚠️ Diretório {mask_dir} não encontrado")
            return True
        
        # Listar arquivos
        img_files = [f for f in os.listdir(img_dir) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
        mask_files = [f for f in os.listdir(mask_dir) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
        
        print(f"📂 Imagens encontradas: {len(img_files)}")
        print(f"📂 Máscaras encontradas: {len(mask_files)}")
        
        if len(img_files) == 0:
            print("⚠️ Nenhuma imagem encontrada")
            return True
        
        # Teste apenas listagem, sem processamento completo
        print("✅ Estrutura de dados reais detectada")
        
        if len(img_files) > 0:
            print(f"📄 Exemplo de arquivo de imagem: {img_files[0]}")
        if len(mask_files) > 0:
            print(f"📄 Exemplo de arquivo de máscara: {mask_files[0]}")
        
        print("💡 Para testar processamento completo, use a GUI ou o example_usage.py")
        
        print("\n🎉 Teste 6: PASSOU")
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def run_all_tests():
    """Executa todos os testes"""
    print("🚀 Executando Bateria de Testes - transforms_fake")
    print("=" * 60)
    
    tests = [
        test_1_basic_import,
        test_2_class_creation,
        test_3_utility_functions,
        test_4_basic_processing,
        test_5_gui_import,
        test_6_with_real_data
    ]
    
    results = []
    
    for test_func in tests:
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"❌ Teste {test_func.__name__} falhou: {e}")
            results.append(False)
    
    # Resumo final
    print("\n" + "=" * 60)
    print("📊 RESUMO DOS TESTES")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    for i, (test_func, result) in enumerate(zip(tests, results), 1):
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"Teste {i}: {test_func.__name__:<25} {status}")
    
    print("-" * 60)
    print(f"🎯 RESULTADO FINAL: {passed}/{total} testes passaram")
    
    if passed == total:
        print("🎉 TODOS OS TESTES PASSARAM! Biblioteca está funcionando.")
    elif passed >= total - 1:
        print("✅ Biblioteca está quase totalmente funcional.")
    elif passed >= total // 2:
        print("⚠️ Biblioteca parcialmente funcional. Verifique os erros.")
    else:
        print("❌ Muitos problemas detectados. Biblioteca precisa de correções.")
    
    return passed, total

def quick_test():
    """Teste rápido - apenas importação e criação básica"""
    print("⚡ Teste Rápido")
    print("-" * 20)
    
    try:
        from transforms_fake import ImageTransformer
        transformer = ImageTransformer()
        print("✅ Biblioteca funcionando!")
        print(f"📦 Tamanho padrão: {transformer.target_size}")
        return True
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Script de Testes - transforms_fake")
    print("Escolha uma opção:")
    print("1. Teste rápido (apenas importação)")
    print("2. Todos os testes")
    print("3. Teste específico")
    
    choice = input("\nDigite sua escolha (1-3): ").strip()
    
    if choice == "1":
        quick_test()
    elif choice == "2":
        run_all_tests()
    elif choice == "3":
        print("\nTestes disponíveis:")
        print("1. Importação básica")
        print("2. Criação de classe")
        print("3. Funções utilitárias")
        print("4. Processamento básico")
        print("5. Interface gráfica")
        print("6. Dados reais")
        
        test_choice = input("Escolha o teste (1-6): ").strip()
        
        tests = [
            test_1_basic_import,
            test_2_class_creation,
            test_3_utility_functions,
            test_4_basic_processing,
            test_5_gui_import,
            test_6_with_real_data
        ]
        
        if test_choice.isdigit() and 1 <= int(test_choice) <= 6:
            tests[int(test_choice) - 1]()
        else:
            print("❌ Escolha inválida")
    else:
        print("❌ Escolha inválida")
        quick_test()  # Executar teste rápido por padrão