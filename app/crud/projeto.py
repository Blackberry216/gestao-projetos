from typing import Optional
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.models.projeto import Projeto
from app.models.projeto_profissional import ProjetoProfissional
from app.schemas.alocacao_schema import AlocacaoCreate
from app.schemas.projeto_schema import ProjetoCreate, ProjetoUpdate


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


def atualizar_projeto(db: Session, projeto_id: int, dados: ProjetoUpdate):
    db_projeto = buscar_projeto_por_id(db, projeto_id=projeto_id)

    if db_projeto is None:
        return None

    for campo, valor in dados.model_dump(exclude_none=True).items():
        setattr(db_projeto, campo, valor)

    db.commit()
    db.refresh(db_projeto)
    return db_projeto


def deletar_projeto(db: Session, projeto_id: int):
    db_projeto = buscar_projeto_por_id(db, projeto_id=projeto_id)

    if db_projeto is None:
        return False

    try:
        db.delete(db_projeto)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise

    return True

def alocar_profissional_no_projeto(db: Session, projeto_id: int, dados: AlocacaoCreate):
    db_alocacao = ProjetoProfissional(
        projeto_id=projeto_id,
        profissional_id=dados.profissional_id,
        responsabilidade=dados.responsabilidade
    )
    db.add(db_alocacao)
    db.commit()
    db.refresh(db_alocacao)
    return db_alocacao

def desalocar_profissional(db: Session, projeto_id: int, profissional_id: int):
    alocacao = db.query(ProjetoProfissional).filter(
        ProjetoProfissional.projeto_id == projeto_id,
        ProjetoProfissional.profissional_id == profissional_id
    ).first()
    
    if alocacao:
        db.delete(alocacao)
        db.commit()
        return True
    return False