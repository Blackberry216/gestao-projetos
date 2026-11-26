from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Profissional(Base):
    __tablename__ = "profissionais"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, nullable=True)
    cargo = Column(String, nullable=False)
    alocacoes = relationship("ProjetoProfissional", back_populates="profissional")
    tarefas = relationship("Tarefa", back_populates="responsavel")