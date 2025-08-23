from sqlalchemy import Column, String, Integer, Float, ForeignKey, Date
from sqlalchemy.orm import relationship

from src.controllers.scrapy import diarias_deputados
from src.database.base import Base

class Diaria(Base):
    __tablename__ = "diarias_deputados"
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_servidor = Column(ForeignKey("servidores.id"), nullable=False)
    cargo = Column(String)
    lotacao = Column(String)
    finalidade = Column(String)
    destino = Column(String)
    data_saida = Column(Date)
    ordem_bancaria = Column(String)
    empenho = Column(String)
    meio_transporte = Column(String)
    numero_diarias = Column(Integer)
    valor_unitario = Column(Float)
    valor_total = Column(Float)

    servidor = relationship("Servidor", back_populates="diarias")
