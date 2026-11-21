from pydantic import BaseModel, Field
from typing import Optional


class ProfissionalCreate(BaseModel):
    nome: str = Field(..., description="Nome do profissional")
    email: Optional[str] = Field(None, description="E-mail do profissional")
    cargo: str = Field(..., description="Cargo ou especialidade (ex: Desenvolvedor, Analista, Testador, Gerente)")


class ProfissionalResponse(ProfissionalCreate):
    id: int

    class Config:
        from_attributes = True