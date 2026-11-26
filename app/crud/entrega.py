from typing import Optional
from sqlalchemy.orm import Session
from app.models.entrega import Entrega
from app.models.tarefa import Tarefa
from app.schemas.entrega_schema import EntregaCreate, EntregaUpdate
from sqlalchemy.exc import IntegrityError

def criar_entrega(db: Session, entrega: EntregaCreate):
    dados_entrega = entrega.model_dump(exclude={"tarefa_ids"})
    
    db_entrega = Entrega(**dados_entrega)
    
    if entrega.tarefa_ids:
        tarefas = db.query(Tarefa).filter(Tarefa.id.in_(entrega.tarefa_ids)).all()
        db_entrega.tarefas = tarefas
    
    db.add(db_entrega)
    db.commit()
    db.refresh(db_entrega)
    return db_entrega

def listar_entregas(db: Session, projeto_id: Optional[int] = None, page: int = 1, size: int = 10):
    query = db.query(Entrega)
    if projeto_id:
        query = query.filter(Entrega.projeto_id == projeto_id)
    
    return query.order_by(Entrega.id).offset((page - 1) * size).limit(size).all()

def buscar_entrega_por_id(db: Session, entrega_id: int):
    return db.query(Entrega).filter(Entrega.id == entrega_id).first()

def atualizar_entrega(db: Session, entrega_id: int, dados: EntregaUpdate):
    db_entrega = buscar_entrega_por_id(db, entrega_id)
    if db_entrega is None:
        return None
    
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(db_entrega, campo, valor)
        
    db.commit()
    db.refresh(db_entrega)
    return db_entrega

def deletar_entrega(db: Session, entrega_id: int):
    db_entrega = buscar_entrega_por_id(db, entrega_id)
    if db_entrega is None:
        return False
        
    try:
        db.delete(db_entrega)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise
    return True