from sqlalchemy import Column, String, Integer, Date, Float, ForeignKey
from sqlalchemy.orm import relationship
from src.database.base import Base

class VerbaIndenizatoria(Base):
    __tablename__ = "verbas_indenizatorias"
    id = Column(Integer, autoincrement=True, primary_key=True)
    id_servidor = Column(ForeignKey("servidores.id"), nullable=False)
    data = Column(Date)
    lote = Column(String)
    total_pago = Column(Float)


    servidor = relationship("Servidor", back_populates="verbas_indenizatorias")
    detalhes = relationship("VerbaIndenizatoriaDetalhes", back_populates="verba_indenizatoria", cascade="all, delete-orphan")



