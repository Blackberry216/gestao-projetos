from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.crud import profissional as crud_profissional
from app.crud import projeto as crud_projeto
from app.schemas.profissional_schema import ProfissionalCreate, ProfissionalUpdate, ProfissionalResponse
from app.schemas.projeto_schema import ProjetoResponse

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
    profissionais = crud_profissional.listar_profissionais(db=db, page=page, size=size, cargo=cargo)
    if not profissionais:
        raise HTTPException(status_code=404, detail="Nenhum profissional encontrado com esses critérios")
    return profissionais


@router.get("/{profissional_id}", response_model=ProfissionalResponse)
def buscar_por_id(profissional_id: int, db: Session = Depends(get_db)):
    db_profissional = crud_profissional.buscar_profissional_por_id(db, profissional_id=profissional_id)

    if db_profissional is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profissional não encontrado"
        )

    return db_profissional


@router.put("/{profissional_id}", response_model=ProfissionalResponse)
def atualizar(profissional_id: int, dados: ProfissionalUpdate, db: Session = Depends(get_db)):
    db_profissional = crud_profissional.atualizar_profissional(db, profissional_id=profissional_id, dados=dados)

    if db_profissional is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profissional não encontrado"
        )

    return db_profissional


@router.delete("/{profissional_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar(profissional_id: int, db: Session = Depends(get_db)):
    try:
        apagado = crud_profissional.deletar_profissional(db, profissional_id=profissional_id)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Não é possível excluir o profissional porque ele possui tarefas ou alocações em projetos"
        )

    if not apagado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profissional não encontrado"
        )


@router.get("/{profissional_id}/projetos", response_model=List[ProjetoResponse])
def listar_projetos_do_profissional(profissional_id: int, db: Session = Depends(get_db)):
    if crud_profissional.buscar_profissional_por_id(db, profissional_id=profissional_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profissional não encontrado"
        )

    return crud_projeto.listar_projetos_do_profissional(db, profissional_id=profissional_id)