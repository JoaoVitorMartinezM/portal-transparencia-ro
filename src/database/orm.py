from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.base import Base
from src.database.models import Servidor

class ORM:

    def __init__(self):
        self.engine = self.connection()
        self.session = None

    def connection(self):
        db_path = Path(__file__).resolve().parent / "portal-transparencia.db"
        return create_engine(f'sqlite:///{str(db_path)}', echo=True)
    
    def __enter__(self):
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        return self
    
    def __exit__(self, exc_type, exc_value, exc_tb):
        self.session.close()
    
    def generateBD(self):
        Base.metadata.create_all(self.engine)
