from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.base import Base
from src.database.models import Servidor
import os

class ORM:

    def __init__(self):
        self.engine = self.connection()
        self.session = None

    def connection(self):
        banco_producao = os.environ.get("BANCO_PROD", None)
        if not banco_producao:
            db_path = Path(__file__).resolve().parent / "portal-transparencia.db"
            return create_engine(f'sqlite:///{str(db_path)}', echo=True)
        return  create_engine(
            banco_producao,
            pool_size=5,  # conexões ativas no pool
            max_overflow=10,  # conexões extras temporárias
            pool_timeout=30,  # tempo de espera antes de dar erro
            pool_recycle=1800,  # reciclar conexões a cada 30min
        )
    
    def __enter__(self):
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        return self
    
    def __exit__(self, exc_type, exc_value, exc_tb):
        self.session.close()
    
    def generateBD(self):
        Base.metadata.create_all(self.engine)
