from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.crud import tarefa as crud_tarefa
from app.crud import dependencia as crud_dependencia
from app.schemas.tarefa_schema import TarefaResponse
from app.schemas.dependencia_schema import DependenciaCreate

router = APIRouter(prefix="/tarefas", tags=["Dependências"])


@router.post(
    "/{tarefa_id}/dependencias",
    response_model=List[TarefaResponse],
    status_code=status.HTTP_201_CREATED,
)
def adicionar(tarefa_id: int, dados: DependenciaCreate, db: Session = Depends(get_db)):
    if crud_tarefa.buscar_tarefa_por_id(db, tarefa_id=tarefa_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarefa não encontrada"
        )

    if crud_tarefa.buscar_tarefa_por_id(db, tarefa_id=dados.depende_de_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarefa da qual esta depende não encontrada"
        )

    if tarefa_id == dados.depende_de_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uma tarefa não pode depender dela mesma"
        )

    if crud_dependencia.dependencia_existe(db, tarefa_id, dados.depende_de_id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Essa dependência já está cadastrada"
        )

    if crud_dependencia.cria_ciclo(db, tarefa_id, dados.depende_de_id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A dependência criaria um ciclo entre tarefas"
        )

    crud_dependencia.adicionar_dependencia(db, tarefa_id, dados.depende_de_id)
    return crud_dependencia.listar_dependencias(db, tarefa_id)


@router.get("/{tarefa_id}/dependencias", response_model=List[TarefaResponse])
def listar(tarefa_id: int, db: Session = Depends(get_db)):
    if crud_tarefa.buscar_tarefa_por_id(db, tarefa_id=tarefa_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarefa não encontrada"
        )

    return crud_dependencia.listar_dependencias(db, tarefa_id)


@router.delete(
    "/{tarefa_id}/dependencias/{depende_de_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remover(tarefa_id: int, depende_de_id: int, db: Session = Depends(get_db)):
    if not crud_dependencia.remover_dependencia(db, tarefa_id, depende_de_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dependência não encontrada"
        )