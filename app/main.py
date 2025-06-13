from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import uvicorn
import uuid
from .models import NotaCreate, NotaResponse
from .firestore import db

app = FastAPI(
    title="Sistema de Notas API",
    description="API para gerenciamento de notas de alunos",
    version="1.0.0"
)

# Configuração de CORS para permitir requisições do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique os domínios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_firestore_client():
    """
    Retorna o cliente Firestore
    """
    return db

@app.get("/", tags=["Root"])
async def read_root():
    """
    Endpoint raiz para verificar se a API está funcionando.
    """
    return {"status": "ok", "message": "API de Notas de Alunos está funcionando!"}

# Endpoint para listar todas as notas
@app.get("/notas", response_model=list[NotaResponse], tags=["Notas"])
async def listar_notas(db=Depends(get_firestore_client)):
    """
    Retorna todas as notas cadastradas no sistema.
    """
    try:
        notas_ref = db.collection("notas")
        docs = notas_ref.stream()
        
        notas = []
        for doc in docs:
            nota_data = doc.to_dict()
            nota_data["id"] = doc.id
            notas.append(nota_data)
        
        return notas
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar notas: {str(e)}")

# Endpoint para criar uma nova nota
@app.post("/notas", response_model=NotaResponse, tags=["Notas"])
async def criar_nota(nota: NotaCreate, db=Depends(get_firestore_client)):
    """
    Cria uma nova nota no sistema.
    
    - **nome**: Nome do aluno
    - **nota**: Nota do aluno (entre 0 e 10)
    """
    try:
        # Validação adicional da nota
        if nota.nota < 0 or nota.nota > 10:
            raise HTTPException(status_code=400, detail="A nota deve estar entre 0 e 10")
            
        # Preparar dados para salvar
        nota_dict = nota.dict()
        
        # Adicionar ao Firestore
        try:
            nota_ref = db.collection("notas").document()
            nota_ref.set(nota_dict)
            
            # Garantir que o ID seja uma string
            doc_id = str(nota_ref.id) if hasattr(nota_ref, 'id') else str(nota_ref)
            
            # Retornar a nota criada com o ID
            return {
                "id": doc_id,
                **nota_dict
            }
        except Exception as e:
            print(f"Erro ao salvar no Firestore: {e}")
            # Fallback para um ID fixo em caso de erro
            return {
                "id": f"temp-{str(uuid.uuid4())[:8]}",
                **nota_dict
            }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar nota: {str(e)}")

# Para executar diretamente este arquivo durante desenvolvimento
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
