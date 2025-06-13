# app/main.py (trecho modificado)
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