import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

try:
    if "FIREBASE_CREDENTIALS" in os.environ:
        print("Usando variável de ambiente FIREBASE_CREDENTIALS")
        cred_json = os.environ.get("FIREBASE_CREDENTIALS")
        cred_dict = json.loads(cred_json)
        cred = credentials.Certificate(cred_dict)
    elif os.path.exists("serviceAccountKey.json"):
        print("Usando arquivo local serviceAccountKey.json")
        cred = credentials.Certificate("serviceAccountKey.json")
    else:
        raise Exception("Credenciais do Firebase não encontradas")
    
    firebase_admin.initialize_app(cred)
    print("Firebase inicializado com sucesso!")
    db = firestore.client()
except Exception as e:
    print(f"ERRO ao inicializar Firebase: {e}")
    class MockDB:
        def collection(self, name):
            class MockCollection:
                def stream(self):
                    return []
                def add(self, data):
                    return [None, MockDoc()]
                def document(self, doc_id=None):
                    return MockDocument(doc_id)
            return MockCollection()
    
    class MockDoc:
        def __init__(self):
            self.id = "mock-id-123" 
        
        def to_dict(self):
            return {}
    
    class MockDocument:
        def __init__(self, doc_id=None):
            self.id = doc_id or "mock-id-123"
        
        def set(self, data):
            return self.id
    
    print("Usando banco de dados simulado para evitar erros de importação")
    db = MockDB()