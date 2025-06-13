# app/models.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Nota(BaseModel):
    nome: str
    nota: float = Field(ge=0, le=10)
    data: Optional[str] = None  # Se não vier, gerar automaticamente

class NotaResponse(Nota):
    id: str
