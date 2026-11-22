from pydantic import BaseModel, Field


class DependenciaCreate(BaseModel):
    depende_de_id: int = Field(..., description="ID da tarefa da qual esta tarefa depende")