from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.crud import tarefa as crud_tarefa
from app.crud import projeto as crud_projeto
from app.crud import profissional as crud_profissional
from app.schemas.tarefa_schema import TarefaCreate, TarefaResponse
from app.schemas.enums import StatusTarefa, Prioridade

router = APIRouter(prefix="/tarefas", tags=["Tarefas"])


@router.post("/", response_model=TarefaResponse, status_code=status.HTTP_201_CREATED)
def criar(tarefa: TarefaCreate, db: Session = Depends(get_db)):
    if crud_projeto.buscar_projeto_por_id(db, projeto_id=tarefa.projeto_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Projeto não encontrado"
        )

    if tarefa.responsavel_id is not None:
        if crud_profissional.buscar_profissional_por_id(db, profissional_id=tarefa.responsavel_id) is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profissional responsável não encontrado"
            )

    return crud_tarefa.criar_tarefa(db=db, tarefa=tarefa)


@router.get("/", response_model=List[TarefaResponse])
def listar(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    status_tarefa: Optional[StatusTarefa] = Query(None, alias="status"),
    prioridade: Optional[Prioridade] = Query(None),
    db: Session = Depends(get_db),
):
    return crud_tarefa.listar_tarefas(
        db=db,
        page=page,
        size=size,
        status=status_tarefa.value if status_tarefa else None,
        prioridade=prioridade.value if prioridade else None,
    )


@router.get("/{tarefa_id}", response_model=TarefaResponse)
def buscar_por_id(tarefa_id: int, db: Session = Depends(get_db)):
    db_tarefa = crud_tarefa.buscar_tarefa_por_id(db, tarefa_id=tarefa_id)

    if db_tarefa is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarefa não encontrada"
        )

    return db_tarefa


@router.get("/{tarefa_id}/dependentes", response_model=List[TarefaResponse])
def listar_dependentes(tarefa_id: int, db: Session = Depends(get_db)):
    if crud_tarefa.buscar_tarefa_por_id(db, tarefa_id=tarefa_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarefa não encontrada"
        )

    return crud_tarefa.listar_tarefas_dependentes(db, tarefa_id=tarefa_id)