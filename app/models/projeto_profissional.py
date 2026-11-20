from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base


class ProjetoProfissional(Base):
    __tablename__ = "projeto_profissional"

    projeto_id = Column(Integer, ForeignKey("projetos.id"), primary_key=True)
    profissional_id = Column(Integer, ForeignKey("profissionais.id"), primary_key=True)
    responsabilidade = Column(String, nullable=False)