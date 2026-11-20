from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud import projeto as crud_projeto
from app.crud import tarefa as crud_tarefa
from app.schemas.projeto_schema import ProjetoCreate, ProjetoResponse
from app.schemas.tarefa_schema import TarefaResponse
from typing import List, Optional

router = APIRouter(prefix="/projetos", tags=["Projetos"])


@router.post("/", response_model=ProjetoResponse, status_code=status.HTTP_201_CREATED)
def criar(projeto: ProjetoCreate, db: Session = Depends(get_db)):
    return crud_projeto.criar_projeto(db=db, projeto=projeto)


@router.get("/", response_model=List[ProjetoResponse])
def listar(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    status_projeto: Optional[str] = Query(None, alias="status"),
    db: Session = Depends(get_db),
):
    return crud_projeto.listar_projetos(db=db, page=page, size=size, status=status_projeto)


@router.get("/{projeto_id}", response_model=ProjetoResponse)
def buscar_por_id(projeto_id: int, db: Session = Depends(get_db)):
    db_projeto = crud_projeto.buscar_projeto_por_id(db, projeto_id=projeto_id)

    if db_projeto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Projeto não encontrado"
        )

    return db_projeto


@router.get("/{projeto_id}/tarefas", response_model=List[TarefaResponse])
def listar_tarefas_do_projeto(projeto_id: int, db: Session = Depends(get_db)):
    if crud_projeto.buscar_projeto_por_id(db, projeto_id=projeto_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Projeto não encontrado"
        )

    return crud_tarefa.listar_tarefas_do_projeto(db, projeto_id=projeto_id)