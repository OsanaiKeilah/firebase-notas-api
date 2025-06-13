from pydantic import BaseModel, Field, validator
from typing import Optional

class NotaCreate(BaseModel):
    nome: str = Field(..., min_length=1, max_length=100, description="Nome do aluno")
    nota: float = Field(..., ge=0, le=10, description="Nota do aluno (entre 0 e 10)")
    
    @validator('nome')
    def nome_nao_vazio(cls, v):
        if not v.strip():
            raise ValueError('O nome não pode estar vazio')
        return v.strip()

class NotaResponse(BaseModel):
    id: str
    nome: str
    nota: float