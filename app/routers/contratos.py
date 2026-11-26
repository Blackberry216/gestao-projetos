from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.contrato import Contrato
from app.crud.projeto import buscar_projeto_por_id
from app.schemas.contrato_schema import ContratoCreate, ContratoResponse

router = APIRouter(prefix="/projetos", tags=["Contratos"])

@router.post("/{projeto_id}/contrato", response_model=ContratoResponse, status_code=status.HTTP_201_CREATED)
def criar_contrato(projeto_id: int, dados: ContratoCreate, db: Session = Depends(get_db)):
    projeto = buscar_projeto_por_id(db, projeto_id=projeto_id)
    if not projeto:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")
        
    if projeto.contrato:
        raise HTTPException(status_code=409, detail="Este projeto já possui um contrato cadastrado")

    novo_contrato = Contrato(
        projeto_id=projeto_id,
        valor_total=dados.valor_total,
        data_assinatura=dados.data_assinatura
    )
    db.add(novo_contrato)
    db.commit()
    db.refresh(novo_contrato)
    return novo_contrato

@router.get("/{projeto_id}/contrato", response_model=ContratoResponse)
def obter_contrato(projeto_id: int, db: Session = Depends(get_db)):
    projeto = buscar_projeto_por_id(db, projeto_id=projeto_id)
    if not projeto:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")
    
    if not projeto.contrato:
        raise HTTPException(status_code=404, detail="Este projeto não possui contrato")
        
    return projeto.contrato