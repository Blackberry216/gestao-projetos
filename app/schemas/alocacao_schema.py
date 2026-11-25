from pydantic import BaseModel, ConfigDict, Field

class AlocacaoCreate(BaseModel):
    profissional_id: int = Field(..., description="ID do profissional a ser alocado")
    responsabilidade: str = Field(..., description="Papel no projeto (ex: Desenvolvedor, Gerente)")

class AlocacaoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    projeto_id: int
    profissional_id: int
    responsabilidade: str