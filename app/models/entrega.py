from sqlalchemy import Column, Integer, String, Date, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.database import Base

entrega_tarefa = Table(
    "entrega_tarefa",
    Base.metadata,
    Column("entrega_id", Integer, ForeignKey("entregas.id"), primary_key=True),
    Column("tarefa_id", Integer, ForeignKey("tarefas.id"), primary_key=True),
)

class Entrega(Base):
    __tablename__ = "entregas"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    descricao = Column(String, nullable=True)
    data_prevista = Column(Date, nullable=False)
    data_realizada = Column(Date, nullable=True)
    status = Column(String, default="Pendente")
    projeto_id = Column(Integer, ForeignKey("projetos.id"), nullable=False)
    projeto = relationship("Projeto", back_populates="entregas")
    tarefas = relationship("Tarefa", secondary=entrega_tarefa, backref="entregas")