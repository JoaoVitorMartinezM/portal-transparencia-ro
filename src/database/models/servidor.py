from src.database.base import Base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

class Servidor(Base):
    __tablename__ = "servidores"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String)
    dsccargo = Column(String)
    dsclotacao = Column(String)

    verbas_indenizatorias = relationship("VerbaIndenizatoria", back_populates="servidor", cascade="all, delete-orphan")
    diarias = relationship("Diaria", back_populates="servidor", cascade="all, delete-orphan")
    remuneracoes = relationship("Remuneracao", back_populates="servidor", cascade="all, delete-orphan")

    def __repr__(self):
        return f'ID: {self.id} NOME: {self.nome}'

    def __eq__(self, other):
        return self.nome == other.nome