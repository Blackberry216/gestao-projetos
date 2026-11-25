from pydantic import BaseModel

class ProfissionalSobrecarregado(BaseModel):
    profissional_id: int
    nome: str
    total_projetos: int