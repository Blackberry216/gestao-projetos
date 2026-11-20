from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.crud import profissional as crud_profissional
from app.schemas.profissional_schema import ProfissionalCreate, ProfissionalResponse

router = APIRouter(prefix="/profissionais", tags=["Profissionais"])


@router.post("/", response_model=ProfissionalResponse, status_code=status.HTTP_201_CREATED)
def criar(profissional: ProfissionalCreate, db: Session = Depends(get_db)):
    return crud_profissional.criar_profissional(db=db, profissional=profissional)


@router.get("/", response_model=List[ProfissionalResponse])
def listar(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    cargo: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    return crud_profissional.listar_profissionais(db=db, page=page, size=size, cargo=cargo)


@router.get("/{profissional_id}", response_model=ProfissionalResponse)
def buscar_por_id(profissional_id: int, db: Session = Depends(get_db)):
    db_profissional = crud_profissional.buscar_profissional_por_id(db, profissional_id=profissional_id)

    if db_profissional is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profissional não encontrado"
        )

    return db_profissional