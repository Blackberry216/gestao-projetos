from typing import Optional
from sqlalchemy.orm import Session
from app.models.projeto import Projeto
from app.models.projeto_profissional import ProjetoProfissional
from app.schemas.projeto_schema import ProjetoCreate


def criar_projeto(db: Session, projeto: ProjetoCreate):
    db_projeto = Projeto(**projeto.model_dump())
    db.add(db_projeto)
    db.commit()
    db.refresh(db_projeto)
    return db_projeto


def listar_projetos(
    db: Session,
    page: int = 1,
    size: int = 10,
    status: Optional[str] = None,
    cliente_id: Optional[int] = None,
):
    query = db.query(Projeto)

    if status:
        query = query.filter(Projeto.status == status)
    if cliente_id:
        query = query.filter(Projeto.cliente_id == cliente_id)

    return query.order_by(Projeto.id).offset((page - 1) * size).limit(size).all()


def buscar_projeto_por_id(db: Session, projeto_id: int):
    return db.query(Projeto).filter(Projeto.id == projeto_id).first()


def listar_projetos_do_profissional(db: Session, profissional_id: int):
    return (
        db.query(Projeto)
        .join(ProjetoProfissional, ProjetoProfissional.projeto_id == Projeto.id)
        .filter(ProjetoProfissional.profissional_id == profissional_id)
        .order_by(Projeto.id)
        .all()
    )