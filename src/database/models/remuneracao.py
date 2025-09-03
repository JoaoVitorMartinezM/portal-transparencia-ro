from src.database.base import Base
from sqlalchemy import Column, String, Integer, ForeignKey, Float, Date
from sqlalchemy.orm import relationship

class Remuneracao(Base):
    __tablename__ = "remuneracoes"

    codigo = Column(Integer, primary_key=True, autoincrement=False, nullable=False)

    remuneracao = Column(Float)
    total_liquido = Column(Float)
    data = Column(Date)

    id_servidor = Column(ForeignKey("servidores.id"), nullable=False)
    servidor = relationship("Servidor", back_populates="remuneracoes")

