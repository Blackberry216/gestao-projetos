from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud import projeto as crud_projeto
from app.schemas.projeto_schema import ProjetoCreate, ProjetoResponse
from typing import List

router = APIRouter(prefix="/projetos", tags=["Projetos"])

@router.post("/", response_model=ProjetoResponse, status_code=status.HTTP_201_CREATED)
def criar(projeto: ProjetoCreate, db: Session = Depends(get_db)):
    return crud_projeto.criar_projeto(db=db, projeto=projeto)

@router.get("/", response_model=List[ProjetoResponse])
def listar(db: Session = Depends(get_db)):
    return crud_projeto.listar_projetos(db=db)

@router.get("/{projeto_id}", response_model=ProjetoResponse)
def buscar_por_id(projeto_id: int, db: Session = Depends(get_db)):
    db_projeto = crud_projeto.buscar_projeto_por_id(db, projeto_id=projeto_id)
    
    if db_projeto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Projeto não encontrado"
        )
        
    return db_projeto