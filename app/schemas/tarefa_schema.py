from datetime import date
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from app.schemas.enums import StatusTarefa, Prioridade


class TarefaCreate(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    titulo: str = Field(..., description="Título da tarefa")
    descricao: Optional[str] = Field(None, description="Descrição da tarefa")
    prazo_previsto: date = Field(..., description="Prazo previsto da tarefa")
    prioridade: Prioridade = Field(Prioridade.media, description="Prioridade da tarefa")
    status: StatusTarefa = Field(StatusTarefa.pendente, description="Situação atual da tarefa")
    projeto_id: int = Field(..., description="ID do projeto da tarefa")
    responsavel_id: Optional[int] = Field(None, description="ID do profissional responsável")


class TarefaResponse(TarefaCreate):
    model_config = ConfigDict(use_enum_values=True, from_attributes=True)

    id: int