from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.models.cliente import Cliente
from app.schemas.cliente_schema import ClienteCreate, ClienteUpdate


def criar_cliente(db: Session, cliente: ClienteCreate):
    db_cliente = Cliente(**cliente.model_dump())
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente


def listar_clientes(db: Session):
    return db.query(Cliente).order_by(Cliente.id).all()


def buscar_cliente_por_id(db: Session, cliente_id: int):
    return db.query(Cliente).filter(Cliente.id == cliente_id).first()


def atualizar_cliente(db: Session, cliente_id: int, dados: ClienteUpdate):
    db_cliente = buscar_cliente_por_id(db, cliente_id=cliente_id)

    if db_cliente is None:
        return None

    for campo, valor in dados.model_dump(exclude_none=True).items():
        setattr(db_cliente, campo, valor)

    db.commit()
    db.refresh(db_cliente)
    return db_cliente


def deletar_cliente(db: Session, cliente_id: int):
    db_cliente = buscar_cliente_por_id(db, cliente_id=cliente_id)

    if db_cliente is None:
        return False

    try:
        db.delete(db_cliente)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise

    return True