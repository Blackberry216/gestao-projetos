from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.tarefa import Tarefa
from app.schemas.enums import StatusTarefa

def calcular_progresso_projeto(db: Session, projeto_id: int):
    total_validas = (
        db.query(func.count(Tarefa.id))
        .filter(
            Tarefa.projeto_id == projeto_id,
            Tarefa.status != StatusTarefa.cancelada.value
        )
        .scalar()
    ) or 0
    
    concluidas = (
        db.query(func.count(Tarefa.id))
        .filter(
            Tarefa.projeto_id == projeto_id,
            Tarefa.status == StatusTarefa.concluida.value
        )
        .scalar()
    ) or 0
    
    if total_validas == 0:
        progresso = 0.0
    else:
        progresso = (concluidas / total_validas) * 100
        
    return {
        "projeto_id": projeto_id,
        "progresso_porcentagem": round(progresso, 2),
        "total_tarefas_validas": total_validas,
        "tarefas_concluidas": concluidas
    }