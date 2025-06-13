# app/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import os

# Verifica se o arquivo de credenciais existe antes de importar
if not os.path.exists("serviceAccountKey.json"):
    print("AVISO: Arquivo serviceAccountKey.json não encontrado!")
    print("Verifique se o arquivo está no local correto:", os.path.abspath("serviceAccountKey.json"))

# Importa os módulos necessários
try:
    from app.firestore import db
    from app.models import Nota, NotaResponse
except Exception as e:
    print(f"ERRO ao importar módulos: {e}")
    raise

app = FastAPI(title="API de Notas de Alunos")

# Libera acesso CORS (para funcionar com seu app Expo)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Troque para o domínio do seu app em produção
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    """Endpoint raiz para verificar se a API está funcionando"""
    return {"status": "ok", "message": "API de Notas de Alunos está funcionando!"}

@app.post("/notas", response_model=NotaResponse)
def criar_nota(nota: Nota):
    try:
        nota_dict = nota.dict()
        nota_dict["dataRegistro"] = nota.data or datetime.now().strftime("%d/%m/%Y %H:%M")

        doc_ref = db.collection("notas").add(nota_dict)
        return NotaResponse(id=doc_ref[1].id, **nota_dict)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao salvar nota: {e}")

@app.get("/notas", response_model=list[NotaResponse])
def listar_notas():
    try:
        docs = db.collection("notas").stream()
        notas = []
        for doc in docs:
            data = doc.to_dict()
            data["id"] = doc.id
            notas.append(NotaResponse(**data))
        return notas
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar notas: {e}")
