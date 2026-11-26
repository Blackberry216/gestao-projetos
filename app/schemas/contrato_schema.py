from pydantic import BaseModel, ConfigDict, Field
from datetime import date
from typing import Optional

class ContratoCreate(BaseModel):
    valor_total: float = Field(..., description="Valor total do contrato")
    data_assinatura: date = Field(..., description="Data de assinatura do contrato")

class ContratoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    projeto_id: int
    valor_total: float
    data_assinatura: date