from pydantic import BaseModel

class ProgressoProjeto(BaseModel):
    projeto_id: int
    progresso_porcentagem: float
    total_tarefas_validas: int
    tarefas_concluidas: int