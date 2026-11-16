from sqlalchemy.orm import Session
from app.models.projeto import Projeto
from app.schemas.projeto_schema import ProjetoCreate

def criar_projeto(db: Session, projeto: ProjetoCreate):
    db_projeto = Projeto(**projeto.model_dump())
    
    db.add(db_projeto)
    db.commit()
    db.refresh(db_projeto)
    
    return db_projeto