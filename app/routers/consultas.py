from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.crud import consulta as crud_consulta
from app.schemas.consulta_schema import ProfissionalSobrecarregado

router = APIRouter(prefix="/consultas", tags=["Consultas Complexas"])

@router.get("/profissionais/sobrecarregados", response_model=List[ProfissionalSobrecarregado])
def profissionais_sobrecarregados(
    x: int = Query(1, description="Quantidade mínima de projetos alocados"), 
    db: Session = Depends(get_db)
):
    return crud_consulta.listar_profissionais_com_mais_de_x_projetos(db=db, x=x)