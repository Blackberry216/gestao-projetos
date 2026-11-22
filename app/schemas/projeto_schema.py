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


class ProjetoUpdate(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    titulo: Optional[str] = Field(None, description="Novo título do projeto")
    objetivo: Optional[str] = Field(None, description="Novo objetivo do projeto")
    prazo_previsto: Optional[date] = Field(None, description="Nova data de término prevista")
    status: Optional[StatusProjeto] = Field(None, description="Novo status do projeto")
    cliente_id: Optional[int] = Field(None, description="Novo cliente do projeto")


class ProjetoResponse(ProjetoCreate):
    model_config = ConfigDict(use_enum_values=True, validate_default=True, from_attributes=True)

    id: int
    data_inicio: date