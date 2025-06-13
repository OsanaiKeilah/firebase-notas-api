"""
Script para verificar a configuração do projeto
"""
import os
import sys
import json

def check_file(filepath, name):
    exists = os.path.exists(filepath)
    print(f"✓ {name}" if exists else f"✗ {name} não encontrado")
    return exists

def main():
    print("\n=== Verificando configuração do Sistema de Notas API ===\n")
    
    # Verifica estrutura de pastas
    print("Estrutura de pastas:")
    app_dir = check_file("app", "Pasta app")
    check_file("app/__init__.py", "app/__init__.py")
    check_file("app/main.py", "app/main.py")
    check_file("app/models.py", "app/models.py")
    check_file("app/firestore.py", "app/firestore.py")
    
    # Verifica arquivo de credenciais
    print("\nArquivo de credenciais:")
    creds_file = check_file("serviceAccountKey.json", "serviceAccountKey.json")
    
    if creds_file:
        try:
            with open("serviceAccountKey.json", "r") as f:
                creds = json.load(f)
                if "type" in creds and "project_id" in creds and "private_key" in creds:
                    print("✓ Formato do arquivo de credenciais parece correto")
                else:
                    print("✗ Arquivo de credenciais parece incompleto")
        except json.JSONDecodeError:
            print("✗ Arquivo de credenciais não é um JSON válido")
        except Exception as e:
            print(f"✗ Erro ao ler arquivo de credenciais: {e}")
    else:
        print("  Caminho esperado:", os.path.abspath("serviceAccountKey.json"))
    
    # Verifica ambiente virtual e dependências
    print("\nAmbiente Python:")
    print(f"✓ Python versão: {sys.version.split()[0]}")
    
    try:
        import firebase_admin
        print(f"✓ firebase-admin instalado (versão {firebase_admin.__version__})")
    except ImportError:
        print("✗ firebase-admin não está instalado")
    
    try:
        import fastapi
        print(f"✓ fastapi instalado (versão {fastapi.__version__})")
    except ImportError:
        print("✗ fastapi não está instalado")
    
    try:
        import uvicorn
        print(f"✓ uvicorn instalado")
    except ImportError:
        print("✗ uvicorn não está instalado")
    
    # Resumo
    print("\nResumo:")
    if not app_dir:
        print("✗ Estrutura de pastas incorreta. Verifique se você está no diretório correto.")
    if not creds_file:
        print("✗ Arquivo de credenciais não encontrado. Baixe-o do console do Firebase.")
    
    print("\nPara executar o servidor:")
    print("  uvicorn app.main:app --reload")
    
    print("\nPara testar a API:")
    print("  Acesse http://localhost:8000/docs no navegador")

if __name__ == "__main__":
    main()
