from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud import projeto as crud_projeto
from app.schemas.projeto_schema import ProjetoCreate, ProjetoResponse

router = APIRouter(prefix="/projetos", tags=["Projetos"])

@router.post("/", response_model=ProjetoResponse, status_code=status.HTTP_201_CREATED)
def criar(projeto: ProjetoCreate, db: Session = Depends(get_db)):
    return crud_projeto.criar_projeto(db=db, projeto=projeto)