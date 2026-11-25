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
from app.services import tarefa_service
router = APIRouter(prefix="/tarefas", tags=["Tarefas"])


@router.post("/", response_model=TarefaResponse, status_code=status.HTTP_201_CREATED)
def criar(tarefa: TarefaCreate, db: Session = Depends(get_db)):
    projeto = crud_projeto.buscar_projeto_por_id(db, projeto_id=tarefa.projeto_id)
    if projeto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Projeto não encontrado"
        )

    if tarefa.prazo_previsto > projeto.prazo_previsto:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"O prazo da tarefa ({tarefa.prazo_previsto}) não pode ultrapassar o prazo do projeto ({projeto.prazo_previsto})."
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
    tarefas = crud_tarefa.listar_tarefas(
        db=db,
        page=page,
        size=size,
        status=status_tarefa.value if status_tarefa else None,
        prioridade=prioridade.value if prioridade else None,
    )
    if not tarefas:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nenhuma tarefa encontrada com esses critérios"
        )
    return tarefas


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
    tarefa_atual = crud_tarefa.buscar_tarefa_por_id(db, tarefa_id=tarefa_id)
    if tarefa_atual is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarefa não encontrada"
        )

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

    projeto_id_alvo = dados.projeto_id if dados.projeto_id is not None else tarefa_atual.projeto_id
    prazo_alvo = dados.prazo_previsto if dados.prazo_previsto is not None else tarefa_atual.prazo_previsto
    
    projeto_alvo = crud_projeto.buscar_projeto_por_id(db, projeto_id=projeto_id_alvo)
    
    if prazo_alvo > projeto_alvo.prazo_previsto:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"O novo prazo da tarefa ({prazo_alvo}) não pode ultrapassar o prazo do projeto ({projeto_alvo.prazo_previsto})."
        )

    if dados.status is not None and dados.status != tarefa_atual.status:
        tarefa_service.validar_rn001_dependencias_concluidas(
            db=db,
            tarefa_id=tarefa_id,
            novo_status=dados.status,
        )
        tarefa_service.validar_rn003_cancelamento_com_dependentes(
            db=db,
            tarefa_id=tarefa_id,
            novo_status=dados.status,
        )

    db_tarefa = crud_tarefa.atualizar_tarefa(db, tarefa_id=tarefa_id, dados=dados)

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

    dependentes = crud_tarefa.listar_tarefas_dependentes(db, tarefa_id=tarefa_id)
    if not dependentes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Esta tarefa não possui dependentes cadastrados"
        )
    return dependentes