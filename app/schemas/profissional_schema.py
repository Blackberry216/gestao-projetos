from pydantic import BaseModel, ConfigDict, Field
from typing import Optional


class ProfissionalCreate(BaseModel):
    nome: str = Field(..., description="Nome do profissional")
    email: Optional[str] = Field(None, description="E-mail do profissional")
    cargo: str = Field(..., description="Cargo ou especialidade (ex: Desenvolvedor, Analista, Testador, Gerente)")


class ProfissionalUpdate(BaseModel):
    nome: Optional[str] = Field(None, description="Novo nome do profissional")
    email: Optional[str] = Field(None, description="Novo e-mail do profissional")
    cargo: Optional[str] = Field(None, description="Novo cargo ou especialidade")


class ProfissionalResponse(ProfissionalCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int