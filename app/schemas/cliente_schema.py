from pydantic import BaseModel, Field
from typing import Optional


class ClienteCreate(BaseModel):
    nome: str = Field(..., description="Nome do cliente")
    setor: Optional[str] = Field(None, description="Setor de atuação do cliente")


class ClienteResponse(ClienteCreate):
    id: int

    class Config:
        from_attributes = True