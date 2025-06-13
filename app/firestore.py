# app/firestore.py
import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

# Verifica se o arquivo de credenciais existe
def check_credentials_file():
    return os.path.exists("serviceAccountKey.json")

# Inicializa Firebase apenas uma vez
if not firebase_admin._apps:
    try:
        # Tenta usar o arquivo serviceAccountKey.json
        if check_credentials_file():
            print("Usando arquivo serviceAccountKey.json para autenticação")
            cred = credentials.Certificate("serviceAccountKey.json")
            firebase_admin.initialize_app(cred)
        else:
            print("ERRO: Arquivo serviceAccountKey.json não encontrado!")
            print("Por favor, coloque o arquivo de credenciais na pasta raiz do projeto.")
            print("Caminho esperado:", os.path.abspath("serviceAccountKey.json"))
            # Não inicializa o app se não tiver credenciais válidas
    except Exception as e:
        print(f"ERRO ao inicializar Firebase: {e}")
        raise

# Obtém o cliente Firestore
try:
    db = firestore.client()
except Exception as e:
    print(f"ERRO ao obter cliente Firestore: {e}")
    # Cria um objeto simulado para evitar erros de importação
    class MockDB:
        def collection(self, name):
            class MockCollection:
                def stream(self):
                    return []
                def add(self, data):
                    return [None, MockDoc()]
            return MockCollection()
    
    class MockDoc:
        def id(self):
            return "mock-id"
    
    print("Usando banco de dados simulado para evitar erros de importação")
    db = MockDB()
