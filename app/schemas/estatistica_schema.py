from pydantic import BaseModel
from typing import Dict

class EstatisticaProjeto(BaseModel):
    projeto_id: int
    total_tarefas: int
    tarefas_por_status: Dict[str, int]
    entregas_previstas: int
    entregas_realizadas: int