from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship

class ProjetoProfissional(Base):
    __tablename__ = "projeto_profissional"

    projeto_id = Column(Integer, ForeignKey("projetos.id"), primary_key=True)
    profissional_id = Column(Integer, ForeignKey("profissionais.id"), primary_key=True)
    responsabilidade = Column(String, nullable=False)
    projeto = relationship("Projeto", back_populates="alocacoes")
    profissional = relationship("Profissional", back_populates="alocacoes")