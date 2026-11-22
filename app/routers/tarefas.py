from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.crud import tarefa as crud_tarefa
from app.crud import projeto as crud_projeto
from app.crud import profissional as crud_profissional
from app.schemas.tarefa_schema import TarefaCreate, TarefaUpdate, TarefaResponse
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


@router.put("/{tarefa_id}", response_model=TarefaResponse)
def atualizar(tarefa_id: int, dados: TarefaUpdate, db: Session = Depends(get_db)):
    if dados.projeto_id is not None:
        if crud_projeto.buscar_projeto_por_id(db, projeto_id=dados.projeto_id) is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Projeto não encontrado"
            )

    if dados.responsavel_id is not None:
        if crud_profissional.buscar_profissional_por_id(db, profissional_id=dados.responsavel_id) is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profissional responsável não encontrado"
            )

    db_tarefa = crud_tarefa.atualizar_tarefa(db, tarefa_id=tarefa_id, dados=dados)

    if db_tarefa is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarefa não encontrada"
        )

    return db_tarefa


@router.delete("/{tarefa_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar(tarefa_id: int, db: Session = Depends(get_db)):
    try:
        apagada = crud_tarefa.deletar_tarefa(db, tarefa_id=tarefa_id)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Não é possível excluir a tarefa porque ela possui dependências cadastradas"
        )

    if not apagada:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarefa não encontrada"
        )


@router.get("/{tarefa_id}/dependentes", response_model=List[TarefaResponse])
def listar_dependentes(tarefa_id: int, db: Session = Depends(get_db)):
    if crud_tarefa.buscar_tarefa_por_id(db, tarefa_id=tarefa_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarefa não encontrada"
        )

    return crud_tarefa.listar_tarefas_dependentes(db, tarefa_id=tarefa_id)