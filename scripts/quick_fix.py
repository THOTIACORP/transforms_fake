#!/usr/bin/env python3
"""
Script para corrigir automaticamente a estrutura do projeto transforms_fake
Execute este arquivo na pasta raiz do projeto
"""

import os
import shutil
import sys

def fix_project_structure():
    """Corrige a estrutura do projeto transforms_fake."""
    
    print("🔧 Corrigindo estrutura do projeto transforms_fake...")
    print("=" * 60)
    
    # Verificar se estamos no diretório correto
    if not os.path.exists("setup.py"):
        print("❌ Erro: Não encontrei setup.py")
        print("   Execute este script na pasta raiz do projeto (onde está o setup.py)")
        return False
    
    success_count = 0
    total_fixes = 0
    
    # 1. Corrigir nome do __init__.py
    total_fixes += 1
    old_init = os.path.join("transforms_fake", "init.py")
    new_init = os.path.join("transforms_fake", "__init__.py")
    
    if os.path.exists(old_init):
        try:
            if os.path.exists(new_init):
                os.remove(new_init)  # Remove se já existir
            os.rename(old_init, new_init)
            print("✅ Corrigido: init.py → __init__.py")
            success_count += 1
        except Exception as e:
            print(f"❌ Erro ao renomear init.py: {e}")
    elif os.path.exists(new_init):
        print("✅ __init__.py já está correto")
        success_count += 1
    else:
        print("⚠️ Aviso: Nem init.py nem __init__.py encontrados")
    
    # 2. Corrigir nome do requirements.txt
    total_fixes += 1
    old_req = "requeriments.txt"
    new_req = "requirements.txt"
    
    if os.path.exists(old_req):
        try:
            if os.path.exists(new_req):
                os.remove(new_req)  # Remove se já existir
            os.rename(old_req, new_req)
            print("✅ Corrigido: requeriments.txt → requirements.txt")
            success_count += 1
        except Exception as e:
            print(f"❌ Erro ao renomear requirements: {e}")
    elif os.path.exists(new_req):
        print("✅ requirements.txt já está correto")
        success_count += 1
    else:
        print("⚠️ Aviso: requirements.txt não encontrado")
    
    # 3. Corrigir MANIFEST.in
    total_fixes += 1
    old_manifest = "manifest_in.txt"
    new_manifest = "MANIFEST.in"
    
    if os.path.exists(old_manifest):
        try:
            if os.path.exists(new_manifest):
                os.remove(new_manifest)  # Remove se já existir
            os.rename(old_manifest, new_manifest)
            print("✅ Corrigido: manifest_in.txt → MANIFEST.in")
            success_count += 1
        except Exception as e:
            print(f"❌ Erro ao renomear MANIFEST: {e}")
    elif os.path.exists(new_manifest):
        print("✅ MANIFEST.in já está correto")
        success_count += 1
    else:
        print("⚠️ Aviso: MANIFEST.in não encontrado")
    
    # 4. Verificar conteúdo do __init__.py
    total_fixes += 1
    init_file = os.path.join("transforms_fake", "__init__.py")
    if os.path.exists(init_file):
        try:
            with open(init_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Verificar se tem o conteúdo mínimo necessário
            if '__version__' not in content or 'ImageTransformer' not in content:
                print("⚠️ __init__.py precisa de conteúdo atualizado")
                
                # Criar conteúdo básico
                init_content = '''"""
transforms_fake - Biblioteca para gerar variações de imagens com objetos rotacionados
"""

__version__ = "1.0.0"
__author__ = "Seu Nome"
__email__ = "seu.email@exemplo.com"

try:
    from .core import ImageTransformer
    from .utils import rotate_image_and_mask, find_background_patch
    
    __all__ = [
        "ImageTransformer",
        "rotate_image_and_mask", 
        "find_background_patch"
    ]
except ImportError as e:
    print(f"Aviso: Erro ao importar módulos: {e}")
    __all__ = []
'''
                
                with open(init_file, 'w', encoding='utf-8') as f:
                    f.write(init_content)
                print("✅ Conteúdo do __init__.py atualizado")
            else:
                print("✅ __init__.py tem conteúdo adequado")
            success_count += 1
        except Exception as e:
            print(f"❌ Erro ao verificar __init__.py: {e}")
    else:
        print("❌ __init__.py não existe")
    
    # 5. Verificar requirements.txt
    total_fixes += 1
    if os.path.exists("requirements.txt"):
        try:
            with open("requirements.txt", 'r', encoding='utf-8') as f:
                content = f.read()
            
            required_deps = ['opencv-python', 'numpy', 'PyQt5']
            missing_deps = [dep for dep in required_deps if dep not in content]
            
            if missing_deps:
                print(f"⚠️ Dependências faltando em requirements.txt: {missing_deps}")
                
                # Criar requirements.txt básico
                req_content = '''opencv-python>=4.5.0
numpy>=1.19.0
PyQt5>=5.15.0
'''
                with open("requirements.txt", 'w', encoding='utf-8') as f:
                    f.write(req_content)
                print("✅ requirements.txt atualizado")
            else:
                print("✅ requirements.txt tem dependências adequadas")
            success_count += 1
        except Exception as e:
            print(f"❌ Erro ao verificar requirements.txt: {e}")
    else:
        print("❌ requirements.txt não existe")
    
    # 6. Limpar arquivos desnecessários
    files_to_remove = [
        "thermal_image_augmenter.py",
        "requirements_variants.txt"
    ]
    
    for file_to_remove in files_to_remove:
        if os.path.exists(file_to_remove):
            try:
                os.remove(file_to_remove)
                print(f"🗑️ Removido arquivo desnecessário: {file_to_remove}")
            except Exception as e:
                print(f"⚠️ Não foi possível remover {file_to_remove}: {e}")
    
    # Resultado final
    print("\n" + "=" * 60)
    print(f"📊 Resultado: {success_count}/{total_fixes} correções aplicadas")
    
    if success_count >= total_fixes - 1:  # Permitir 1 erro
        print("✅ Estrutura corrigida com sucesso!")
        
        print("\n📋 Próximos passos:")
        print("1. pip install -e .")
        print("2. python -c \"from transforms_fake import ImageTransformer; print('✅ Sucesso!')\"")
        print("3. transforms-fake-gui")
        
        # Tentar instalar automaticamente
        try:
            print("\n🔄 Tentando instalação automática...")
            import subprocess
            result = subprocess.run([sys.executable, "-m", "pip", "install", "-e", "."], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Instalação automática bem-sucedida!")
                
                # Testar importação
                try:
                    import transforms_fake
                    print("✅ Teste de importação bem-sucedido!")
                    print(f"📦 Versão: {getattr(transforms_fake, '__version__', 'desconhecida')}")
                except ImportError as e:
                    print(f"⚠️ Erro na importação: {e}")
                    print("   Isso pode ser normal se os módulos core.py/utils.py estão incompletos")
            else:
                print(f"⚠️ Instalação automática falhou:")
                print(result.stderr)
                print("Execute manualmente: pip install -e .")
                
        except Exception as e:
            print(f"⚠️ Erro na instalação automática: {e}")
        
        return True
    else:
        print("❌ Ainda há problemas na estrutura")
        return False

def show_current_structure():
    """Mostra a estrutura atual do projeto."""
    print("\n📁 Estrutura atual do projeto:")
    print("-" * 40)
    
    for root, dirs, files in os.walk("."):
        # Pular diretórios desnecessários
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
        
        level = root.replace(".", "").count(os.sep)
        indent = " " * 2 * level
        print(f"{indent}{os.path.basename(root)}/")
        
        subindent = " " * 2 * (level + 1)
        for file in files:
            if not file.startswith('.') and not file.endswith('.pyc'):
                print(f"{subindent}{file}")

def main():
    """Função principal."""
    print("🚀 Script de Correção - transforms_fake")
    print("Este script irá corrigir automaticamente a estrutura do projeto")
    print("=" * 60)
    
    # Mostrar estrutura atual
    show_current_structure()
    
    # Perguntar confirmação
    response = input("\n❓ Deseja prosseguir com as correções? (s/N): ").strip().lower()
    
    if response in ['s', 'sim', 'y', 'yes']:
        success = fix_project_structure()
        
        if success:
            print("\n🎉 Projeto corrigido e pronto para uso!")
        else:
            print("\n⚠️ Algumas correções falharam. Verifique manualmente.")
            
        # Mostrar estrutura final
        print("\n📁 Estrutura final:")
        show_current_structure()
        
    else:
        print("⏹️ Operação cancelada pelo usuário")

if __name__ == "__main__":
    main()
    
    # Manter janela aberta no Windows
    if sys.platform.startswith('win'):
        input("\nPressione Enter para fechar...")