from sqlalchemy import Column, Integer, String, Date, ForeignKey
import datetime
from app.database import Base


class Projeto(Base):
    __tablename__ = "projetos"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    objetivo = Column(String, nullable=True)
    data_inicio = Column(Date, default=datetime.date.today)
    prazo_previsto = Column(Date, nullable=False)
    status = Column(String, default="Planeado")
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=True)