from src.database.base import Base
from sqlalchemy import Column, String, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship

class Remuneracao(Base):
    __tablename__ = "remuneracoes"

    codigo = Column(Integer, primary_key=True, autoincrement=False, nullable=False)

    remuneracao = Column(Float)
    total_liquido = Column(Float)

    id_servidor = Column(ForeignKey("servidores.id"), nullable=False)
    servidor = relationship("Servidor", back_populates="remuneracoes")

