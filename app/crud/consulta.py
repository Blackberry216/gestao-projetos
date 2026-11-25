from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.profissional import Profissional
from app.models.projeto_profissional import ProjetoProfissional

def listar_profissionais_com_mais_de_x_projetos(db: Session, x: int):
    resultado = (
        db.query(
            Profissional.id.label("profissional_id"),
            Profissional.nome,
            func.count(ProjetoProfissional.projeto_id).label("total_projetos")
        )
        .join(ProjetoProfissional, ProjetoProfissional.profissional_id == Profissional.id)
        .group_by(Profissional.id, Profissional.nome)
        .having(func.count(ProjetoProfissional.projeto_id) > x)
        .order_by(func.count(ProjetoProfissional.projeto_id).desc())
        .all()
    )
    
    return resultado