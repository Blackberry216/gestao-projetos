from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class ProjetoCreate(BaseModel):
    titulo: str = Field(..., description="Título do projeto")
    objetivo: Optional[str] = Field(None, description="Objetivo do projeto")
    prazo_previsto: date = Field(..., description="Data de término prevista")
    status: Optional[str] = Field("Planeado", description="Status atual do projeto")

class ProjetoResponse(ProjetoCreate):
    id: int
    data_inicio: date

    class Config:
        from_attributes = True