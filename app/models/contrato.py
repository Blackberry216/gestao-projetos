from sqlalchemy import Column, Integer, Numeric, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.database import Base

class Contrato(Base):
    __tablename__ = "contratos"

    id = Column(Integer, primary_key=True, index=True)
    projeto_id = Column(Integer, ForeignKey("projetos.id"), unique=True, nullable=False)
    valor_total = Column(Numeric(12, 2), nullable=False)
    data_assinatura = Column(Date, nullable=False)

    projeto = relationship("Projeto", back_populates="contrato")