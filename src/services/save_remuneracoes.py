from sqlalchemy.orm.session import Session

from src.controllers.scrapy import remuneracao_deputados
from datetime import date
from src.database.models import Servidor
from src.database.models.remuneracao import Remuneracao
from src.database.orm import ORM
from sqlalchemy import func

from src.utils.similaridade import similaridade


def save_remuneracoes():

    data = date(day=1, month=6, year=2025)

    remuneracoes_json = remuneracao_deputados(data)

    for r in remuneracoes_json:

        codigo = r.get("codigo", None)

        with ORM() as db:
            session: Session= db.session

            id_remuneracao = session.query(Remuneracao.codigo).where(Remuneracao.codigo == codigo).scalar()

            if id_remuneracao:
                continue

            remuneracao = r.get("remuneracao", None)
            total_liquido = r.get("totalliq", None)
            deputado = r.get("nome", None)

            id_servidor = similaridade(session, deputado)
            if not id_servidor:
                novo_servidor = Servidor(nome=deputado)
                session.add(novo_servidor)
                session.commit()
                id_servidor = novo_servidor.id

            remuneracao_model = Remuneracao(codigo=codigo, remuneracao=remuneracao, total_liquido=total_liquido, id_servidor=id_servidor)
            session.add(remuneracao_model)
            session.commit()


