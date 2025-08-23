from sqlalchemy import Column, String, Integer, Date, Float, ForeignKey
from sqlalchemy.orm import relationship
from src.database.base import Base

class VerbaIndenizatoriaDetalhes(Base):
    __tablename__ = "verbas_indenizatorias_detalhes"
    id = Column(Integer, autoincrement=True, primary_key=True)
    id_verba_indenizatoria = Column(ForeignKey("verbas_indenizatorias.id"), nullable=False)

    prestador = Column(String)
    classe = Column(String)
    data = Column(Date)
    valor = Column(Float)

    verba_indenizatoria = relationship("VerbaIndenizatoria", back_populates="detalhes")

