from pydantic import BaseModel, ConfigDict, Field
from typing import Optional


class ClienteCreate(BaseModel):
    nome: str = Field(..., description="Nome do cliente")
    setor: Optional[str] = Field(None, description="Setor de atuação do cliente")


class ClienteUpdate(BaseModel):
    nome: Optional[str] = Field(None, description="Novo nome do cliente")
    setor: Optional[str] = Field(None, description="Novo setor de atuação do cliente")


class ClienteResponse(ClienteCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int