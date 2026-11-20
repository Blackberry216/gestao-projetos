from typing import Optional
from sqlalchemy.orm import Session
from app.models.projeto import Projeto
from app.schemas.projeto_schema import ProjetoCreate


def criar_projeto(db: Session, projeto: ProjetoCreate):
    db_projeto = Projeto(**projeto.model_dump())
    db.add(db_projeto)
    db.commit()
    db.refresh(db_projeto)
    return db_projeto


def listar_projetos(db: Session, page: int = 1, size: int = 10, status: Optional[str] = None):
    query = db.query(Projeto)
    if status:
        query = query.filter(Projeto.status == status)
    return query.order_by(Projeto.id).offset((page - 1) * size).limit(size).all()


def buscar_projeto_por_id(db: Session, projeto_id: int):
    return db.query(Projeto).filter(Projeto.id == projeto_id).first()