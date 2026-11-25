from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud import projeto as crud_projeto
from app.crud import tarefa as crud_tarefa
from app.crud import cliente as crud_cliente
from app.crud import profissional as crud_profissional
from app.models.projeto_profissional import ProjetoProfissional
from app.schemas.projeto_schema import ProjetoCreate, ProjetoUpdate, ProjetoResponse
from app.schemas.tarefa_schema import TarefaResponse
from app.schemas.enums import StatusProjeto
from app.schemas.alocacao_schema import AlocacaoCreate, AlocacaoResponse
from app.schemas.progresso_schema import ProgressoProjeto
from app.services import projeto_service
from typing import List, Optional

router = APIRouter(prefix="/projetos", tags=["Projetos"])


@router.post("/", response_model=ProjetoResponse, status_code=status.HTTP_201_CREATED)
def criar(projeto: ProjetoCreate, db: Session = Depends(get_db)):
    if projeto.cliente_id is not None:
        if crud_cliente.buscar_cliente_por_id(db, cliente_id=projeto.cliente_id) is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente não encontrado"
            )

    return crud_projeto.criar_projeto(db=db, projeto=projeto)


@router.get("/", response_model=List[ProjetoResponse])
def listar(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    status_projeto: Optional[StatusProjeto] = Query(None, alias="status"),
    cliente_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
):
    return crud_projeto.listar_projetos(
        db=db,
        page=page,
        size=size,
        status=status_projeto.value if status_projeto else None,
        cliente_id=cliente_id,
    )


@router.get("/{projeto_id}", response_model=ProjetoResponse)
def buscar_por_id(projeto_id: int, db: Session = Depends(get_db)):
    db_projeto = crud_projeto.buscar_projeto_por_id(db, projeto_id=projeto_id)

    if db_projeto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Projeto não encontrado"
        )

    return db_projeto


@router.put("/{projeto_id}", response_model=ProjetoResponse)
def atualizar(projeto_id: int, dados: ProjetoUpdate, db: Session = Depends(get_db)):
    if dados.cliente_id is not None:
        if crud_cliente.buscar_cliente_por_id(db, cliente_id=dados.cliente_id) is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente não encontrado"
            )

    db_projeto = crud_projeto.atualizar_projeto(db, projeto_id=projeto_id, dados=dados)

    if db_projeto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Projeto não encontrado"
        )

    return db_projeto


@router.delete("/{projeto_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar(projeto_id: int, db: Session = Depends(get_db)):
    try:
        apagado = crud_projeto.deletar_projeto(db, projeto_id=projeto_id)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Não é possível excluir o projeto porque ele possui tarefas ou profissionais alocados"
        )

    if not apagado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Projeto não encontrado"
        )


@router.get("/{projeto_id}/tarefas", response_model=List[TarefaResponse])
def listar_tarefas_do_projeto(projeto_id: int, db: Session = Depends(get_db)):
    if crud_projeto.buscar_projeto_por_id(db, projeto_id=projeto_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Projeto não encontrado"
        )

    return crud_tarefa.listar_tarefas_do_projeto(db, projeto_id=projeto_id)

@router.post("/{projeto_id}/equipe", response_model=AlocacaoResponse, status_code=status.HTTP_201_CREATED)
def alocar_equipe(projeto_id: int, dados: AlocacaoCreate, db: Session = Depends(get_db)):
    if crud_projeto.buscar_projeto_por_id(db, projeto_id=projeto_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Projeto não encontrado")
        
    if crud_profissional.buscar_profissional_por_id(db, profissional_id=dados.profissional_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profissional não encontrado")
        
    alocacao_existente = db.query(ProjetoProfissional).filter(
        ProjetoProfissional.projeto_id == projeto_id,
        ProjetoProfissional.profissional_id == dados.profissional_id
    ).first()
    
    if alocacao_existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail="Este profissional já está alocado neste projeto"
        )

    return crud_projeto.alocar_profissional_no_projeto(db=db, projeto_id=projeto_id, dados=dados)

@router.get("/{projeto_id}/progresso", response_model=ProgressoProjeto)
def obter_progresso(projeto_id: int, db: Session = Depends(get_db)):
    if crud_projeto.buscar_projeto_por_id(db, projeto_id=projeto_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Projeto não encontrado"
        )
        
    return projeto_service.calcular_progresso_projeto(db=db, projeto_id=projeto_id)

@router.delete("/{projeto_id}/equipe/{profissional_id}", status_code=status.HTTP_204_NO_CONTENT)
def desalocar_equipe(projeto_id: int, profissional_id: int, db: Session = Depends(get_db)):
    if crud_projeto.buscar_projeto_por_id(db, projeto_id=projeto_id) is None:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")
        
    sucesso = crud_projeto.desalocar_profissional(db=db, projeto_id=projeto_id, profissional_id=profissional_id)
    
    if not sucesso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Este profissional não está alocado neste projeto"
        )
    return None