from fastapi import APIRouter, Depends, Query, status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.crud import consulta as crud_consulta
from app.crud import projeto as crud_projeto
from app.schemas.consulta_schema import ProfissionalSobrecarregado
from app.schemas.tarefa_schema import TarefaResponse

router = APIRouter(prefix="/consultas", tags=["Consultas Complexas"])

@router.get("/profissionais/sobrecarregados", response_model=List[ProfissionalSobrecarregado])
def profissionais_sobrecarregados(
    x: int = Query(1, description="Quantidade mínima de projetos alocados"), 
    db: Session = Depends(get_db)
):
    return crud_consulta.listar_profissionais_com_mais_de_x_projetos(db=db, x=x)

@router.get("/projetos/{projeto_id}/tarefas-atrasadas", response_model=List[TarefaResponse])
def obter_tarefas_atrasadas(projeto_id: int, db: Session = Depends(get_db)):
    if crud_projeto.buscar_projeto_por_id(db, projeto_id=projeto_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Projeto não encontrado"
        )
    return crud_consulta.listar_tarefas_atrasadas_do_projeto(db=db, projeto_id=projeto_id)