from typing import List
from src.database.orm import ORM
from src.database.models import Servidor

def save_servidores(servidores: List[Servidor]):
    with ORM() as db:
        session = db.session
        todos_servidores = session.query(Servidor).all()

        # Converte dicionario do python para a classe Servidor
        models = list(map(lambda s: Servidor(**s), servidores))

        filtro = list(filter(lambda m: m not in todos_servidores, models))

        session.add_all(filtro)
        session.commit()
