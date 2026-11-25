from pydantic import BaseModel, ConfigDict, Field
from datetime import date
from typing import Optional, List
from app.schemas.enums import StatusEntrega

class EntregaCreate(BaseModel):
    titulo: str = Field(..., description="Título da entrega")
    descricao: Optional[str] = Field(None, description="Descrição da entrega")
    data_prevista: date = Field(..., description="Data prevista para entrega")
    projeto_id: int = Field(..., description="ID do projeto ao qual a entrega pertence")
    tarefa_ids: List[int] = Field(default=[], description="IDs das tarefas vinculadas a esta entrega")

class EntregaUpdate(BaseModel):
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    data_prevista: Optional[date] = None
    status: Optional[StatusEntrega] = None
    data_realizada: Optional[date] = None

class EntregaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    titulo: str
    descricao: Optional[str]
    data_prevista: date
    data_realizada: Optional[date]
    status: str
    projeto_id: int