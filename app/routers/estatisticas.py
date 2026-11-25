from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.crud import estatistica as crud_estatistica
from app.crud.projeto import buscar_projeto_por_id
from app.schemas.estatistica_schema import EstatisticaProjeto

router = APIRouter(prefix="/estatisticas", tags=["Estatísticas"])

@router.get("/projetos/{projeto_id}", response_model=EstatisticaProjeto)
def obter_estatisticas(projeto_id: int, db: Session = Depends(get_db)):
    projeto = buscar_projeto_por_id(db, projeto_id=projeto_id)
    if projeto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Projeto não encontrado para gerar estatísticas."
        )
        
    return crud_estatistica.obter_estatisticas_projeto(db=db, projeto_id=projeto_id)