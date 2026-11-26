from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.crud import cliente as crud_cliente
from app.schemas.cliente_schema import ClienteCreate, ClienteUpdate, ClienteResponse

router = APIRouter(prefix="/clientes", tags=["Clientes"])


@router.post("/", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
def criar(cliente: ClienteCreate, db: Session = Depends(get_db)):
    return crud_cliente.criar_cliente(db=db, cliente=cliente)


@router.get("/", response_model=List[ClienteResponse])
def listar(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    clientes = crud_cliente.listar_clientes(db=db, page=page, size=size)
    if not clientes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nenhum cliente encontrado nesta página"
        )
    return clientes


@router.get("/{cliente_id}", response_model=ClienteResponse)
def buscar_por_id(cliente_id: int, db: Session = Depends(get_db)):
    db_cliente = crud_cliente.buscar_cliente_por_id(db, cliente_id=cliente_id)

    if db_cliente is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado"
        )

    return db_cliente


@router.put("/{cliente_id}", response_model=ClienteResponse)
def atualizar(cliente_id: int, dados: ClienteUpdate, db: Session = Depends(get_db)):
    db_cliente = crud_cliente.atualizar_cliente(db, cliente_id=cliente_id, dados=dados)

    if db_cliente is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado"
        )

    return db_cliente


@router.delete("/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar(cliente_id: int, db: Session = Depends(get_db)):
    try:
        apagado = crud_cliente.deletar_cliente(db, cliente_id=cliente_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Não é possível excluir o cliente porque ele possui projetos vinculados."
        )

    if not apagado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado")