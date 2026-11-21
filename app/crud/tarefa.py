from typing import Optional
from sqlalchemy.orm import Session
from app.models.tarefa import Tarefa, dependencia_tarefa
from app.schemas.tarefa_schema import TarefaCreate


def criar_tarefa(db: Session, tarefa: TarefaCreate):
    db_tarefa = Tarefa(**tarefa.model_dump())
    db.add(db_tarefa)
    db.commit()
    db.refresh(db_tarefa)
    return db_tarefa


def listar_tarefas(
    db: Session,
    page: int = 1,
    size: int = 10,
    status: Optional[str] = None,
    prioridade: Optional[str] = None,
):
    query = db.query(Tarefa)

    if status:
        query = query.filter(Tarefa.status == status)
    if prioridade:
        query = query.filter(Tarefa.prioridade == prioridade)

    return query.order_by(Tarefa.id).offset((page - 1) * size).limit(size).all()


def buscar_tarefa_por_id(db: Session, tarefa_id: int):
    return db.query(Tarefa).filter(Tarefa.id == tarefa_id).first()


def listar_tarefas_do_projeto(db: Session, projeto_id: int):
    return (
        db.query(Tarefa)
        .filter(Tarefa.projeto_id == projeto_id)
        .order_by(Tarefa.id)
        .all()
    )


def listar_tarefas_dependentes(db: Session, tarefa_id: int):
    return (
        db.query(Tarefa)
        .join(dependencia_tarefa, dependencia_tarefa.c.tarefa_id == Tarefa.id)
        .filter(dependencia_tarefa.c.depende_de_id == tarefa_id)
        .order_by(Tarefa.id)
        .all()
    )