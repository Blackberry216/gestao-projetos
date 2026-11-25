from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.tarefa import Tarefa
from app.models.entrega import Entrega

def obter_estatisticas_projeto(db: Session, projeto_id: int):
    resultado_tarefas = (
        db.query(Tarefa.status, func.count(Tarefa.id))
        .filter(Tarefa.projeto_id == projeto_id)
        .group_by(Tarefa.status)
        .all()
    )
    
    tarefas_por_status = {status: count for status, count in resultado_tarefas}
    total_tarefas = sum(tarefas_por_status.values())
    
    total_previstas = (
        db.query(func.count(Entrega.id))
        .filter(Entrega.projeto_id == projeto_id)
        .scalar()
    ) or 0
    
    total_realizadas = (
        db.query(func.count(Entrega.id))
        .filter(Entrega.projeto_id == projeto_id, Entrega.data_realizada.isnot(None))
        .scalar()
    ) or 0
    
    return {
        "projeto_id": projeto_id,
        "total_tarefas": total_tarefas,
        "tarefas_por_status": tarefas_por_status,
        "entregas_previstas": total_previstas,
        "entregas_realizadas": total_realizadas
    }