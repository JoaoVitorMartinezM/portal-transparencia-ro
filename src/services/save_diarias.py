from datetime import date

from sqlalchemy.orm.session import Session
from sqlalchemy import or_, func, and_
from src.controllers.scrapy import diarias_deputados
from src.database.models import Servidor
from src.database.models.diaria import Diaria
from src.database.orm import ORM
from src.utils.similaridade import similaridade


# def nome_filter(nome, coluna):
#     partes = nome.split()
#     conditions = [coluna.ilike(f"%{parte}%") for parte in partes]
#     return or_(*conditions)  # exige que todas as partes estejam presentes

# def nome_filter(nome, coluna, min_matches=2):
#     partes = nome.split()
#     conditions = [coluna.ilike(f"%{parte}%") for parte in partes]
#
#     if not conditions:
#         return None
#
#     # Se tiver poucas partes, reduz o min_matches
#     min_matches = min(min_matches, len(conditions))
#
#     # Gera combinações de condições com pelo menos `min_matches` partes
#     grupos = []
#     for i in range(len(conditions)):
#         for j in range(i + 1, len(conditions)):
#             if min_matches == 2:
#                 grupos.append(and_(conditions[i], conditions[j]))
#             # se no futuro quiser mais de 2 matches, poderia usar itertools.combinations
#
#     if min_matches == 1:
#         return or_(*conditions)
#     else:
#         return or_(*grupos)

def save_diarias():
    data = date(day=1, month=9, year=2025)
    diarias_list = diarias_deputados(data)



    def map_diarias_dict_to_model(item: dict):
        id_servidor = 0
        with ORM() as db:
            session: Session = db.session
            # id_servidor = session.query(Servidor.id
            #                             ).filter(nome_filter(item["Deputado"], Servidor.nome, min_matches=2)
            #                                      ).order_by(func.char_length(Servidor.nome)).first()[0]
            id_servidor = similaridade(session, item.get("Deputado", None))
            if not id_servidor:
                novo_servidor = Servidor(nome=item.get("Deputado", None))
                session.add(novo_servidor)
                session.commit()
                id_servidor = novo_servidor.id

            diaria_db = session.query(Diaria).where(Diaria.destino == item.get("Destino", None), Diaria.id_servidor == id_servidor,
                                           Diaria.valor_total == item.get("Total", None)).first()
            if diaria_db:
                return diaria_db

            model = Diaria(
                id_servidor=id_servidor,
                cargo=item.get("Cargo", None),
                lotacao=item.get("Lotação", None),
                finalidade=item.get("Finalidade", None),
                destino=item.get("Destino", None),
                data_saida=item.get("Dt. Saída", None),
                ordem_bancaria=item.get("Ordem Bancária", None),
                empenho=item.get("Empenho", None),
                meio_transporte=item.get("Meio Transporte", None),
                numero_diarias=item.get("Número de Diárias", None),
                valor_unitario=item.get("Valor Unitário", None),
                valor_total=item.get("Total", None),
            )
            session.add(model)
            session.commit()
            return model

    diarias_model_list = list(map(map_diarias_dict_to_model, diarias_list))