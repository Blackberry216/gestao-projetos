from datetime import date
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from app.schemas.enums import StatusProjeto


class ProjetoCreate(BaseModel):
    model_config = ConfigDict(use_enum_values=True, validate_default=True)

    titulo: str = Field(..., description="Título do projeto")
    objetivo: Optional[str] = Field(None, description="Objetivo do projeto")
    prazo_previsto: date = Field(..., description="Data de término prevista")
    status: StatusProjeto = Field(StatusProjeto.planejado, description="Status atual do projeto")
    cliente_id: Optional[int] = Field(None, description="ID do cliente do projeto")


class ProjetoResponse(ProjetoCreate):
    model_config = ConfigDict(use_enum_values=True, validate_default=True, from_attributes=True)

    id: int
    data_inicio: date