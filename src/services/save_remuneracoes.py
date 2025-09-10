from sqlalchemy.orm.session import Session

from src.controllers.scrapy import remuneracao_deputados
from datetime import date
from src.database.models import Servidor
from src.database.models.remuneracao import Remuneracao
from src.database.orm import ORM
from sqlalchemy import func

from src.utils.similaridade import similaridade


def save_remuneracoes():
    data = date.today()

    remuneracoes_json = remuneracao_deputados(data)
    print(remuneracoes_json)
    for json_data in remuneracoes_json:
        for key, value in json_data.items():
            mes, ano = key.split('-')
            data = date(day=1, month=int(mes), year=int(ano))
            for r in value:
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

                    remuneracao_model = Remuneracao(codigo=codigo, remuneracao=remuneracao, total_liquido=total_liquido, id_servidor=id_servidor, data=data)
                    session.add(remuneracao_model)
                    session.commit()


