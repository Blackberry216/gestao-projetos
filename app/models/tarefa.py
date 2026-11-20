from sqlalchemy import Column, Integer, String, Date, ForeignKey, Table
from app.database import Base

dependencia_tarefa = Table(
    "dependencia_tarefa",
    Base.metadata,
    Column("tarefa_id", Integer, ForeignKey("tarefas.id"), primary_key=True),
    Column("depende_de_id", Integer, ForeignKey("tarefas.id"), primary_key=True),
)


class Tarefa(Base):
    __tablename__ = "tarefas"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    descricao = Column(String, nullable=True)
    prazo_previsto = Column(Date, nullable=False)
    prioridade = Column(String, default="Media")
    status = Column(String, default="Pendente")
    projeto_id = Column(Integer, ForeignKey("projetos.id"), nullable=False)
    responsavel_id = Column(Integer, ForeignKey("profissionais.id"), nullable=True)