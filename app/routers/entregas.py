from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.crud import entrega as crud_entrega
from app.schemas.entrega_schema import EntregaCreate, EntregaResponse, EntregaUpdate

router = APIRouter(prefix="/entregas", tags=["Entregas"])

@router.post("/", response_model=EntregaResponse, status_code=status.HTTP_201_CREATED)
def criar(entrega: EntregaCreate, db: Session = Depends(get_db)):
    return crud_entrega.criar_entrega(db=db, entrega=entrega)

@router.get("/", response_model=List[EntregaResponse])
def listar(projeto_id: Optional[int] = None, db: Session = Depends(get_db)):
    return crud_entrega.listar_entregas(db=db, projeto_id=projeto_id)

@router.get("/{entrega_id}", response_model=EntregaResponse)
def buscar_por_id(entrega_id: int, db: Session = Depends(get_db)):
    db_entrega = crud_entrega.buscar_entrega_por_id(db, entrega_id=entrega_id)
    if db_entrega is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entrega não encontrada")
    return db_entrega

@router.put("/{entrega_id}", response_model=EntregaResponse)
def atualizar(entrega_id: int, entrega: EntregaUpdate, db: Session = Depends(get_db)):
    db_entrega = crud_entrega.atualizar_entrega(db=db, entrega_id=entrega_id, dados=entrega)
    if db_entrega is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entrega não encontrada")
    return db_entrega

@router.delete("/{entrega_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar(entrega_id: int, db: Session = Depends(get_db)):
    sucesso = crud_entrega.deletar_entrega(db=db, entrega_id=entrega_id)
    if not sucesso:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entrega não encontrada")
    return None