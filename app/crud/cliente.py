from sqlalchemy.orm import Session
from app.models.cliente import Cliente
from app.schemas.cliente_schema import ClienteCreate


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