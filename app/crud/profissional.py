from typing import Optional
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.models.profissional import Profissional
from app.schemas.profissional_schema import ProfissionalCreate, ProfissionalUpdate


def criar_profissional(db: Session, profissional: ProfissionalCreate):
    db_profissional = Profissional(**profissional.model_dump())
    db.add(db_profissional)
    db.commit()
    db.refresh(db_profissional)
    return db_profissional


def listar_profissionais(db: Session, page: int = 1, size: int = 10, cargo: Optional[str] = None):
    query = db.query(Profissional)

    if cargo:
        query = query.filter(Profissional.cargo == cargo)

    return query.order_by(Profissional.id).offset((page - 1) * size).limit(size).all()


def buscar_profissional_por_id(db: Session, profissional_id: int):
    return db.query(Profissional).filter(Profissional.id == profissional_id).first()


def atualizar_profissional(db: Session, profissional_id: int, dados: ProfissionalUpdate):
    db_profissional = buscar_profissional_por_id(db, profissional_id=profissional_id)

    if db_profissional is None:
        return None

    for campo, valor in dados.model_dump(exclude_none=True).items():
        setattr(db_profissional, campo, valor)

    db.commit()
    db.refresh(db_profissional)
    return db_profissional


def deletar_profissional(db: Session, profissional_id: int):
    db_profissional = buscar_profissional_por_id(db, profissional_id=profissional_id)

    if db_profissional is None:
        return False

    try:
        db.delete(db_profissional)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise

    return True