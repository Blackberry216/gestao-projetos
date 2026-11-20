from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.crud import cliente as crud_cliente
from app.schemas.cliente_schema import ClienteCreate, ClienteResponse

router = APIRouter(prefix="/clientes", tags=["Clientes"])


@router.post("/", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
def criar(cliente: ClienteCreate, db: Session = Depends(get_db)):
    return crud_cliente.criar_cliente(db=db, cliente=cliente)


@router.get("/", response_model=List[ClienteResponse])
def listar(db: Session = Depends(get_db)):
    return crud_cliente.listar_clientes(db=db)


@router.get("/{cliente_id}", response_model=ClienteResponse)
def buscar_por_id(cliente_id: int, db: Session = Depends(get_db)):
    db_cliente = crud_cliente.buscar_cliente_por_id(db, cliente_id=cliente_id)

    if db_cliente is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado"
        )

    return db_cliente