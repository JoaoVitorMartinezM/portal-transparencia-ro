import json
import os

from flask import Flask, request
from flask import jsonify
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.expression import select, desc
from sqlalchemy.sql.functions import func

from src.database.models import Servidor, Remuneracao, Diaria, VerbaIndenizatoria

from src.database.orm import ORM

app = Flask(__name__)

@app.route("/salarios/total-liquido")
def salarios_total_liquido():
    with ORM() as db:
        session: Session = db.session

        stmt = select(
            Servidor.nome,
            Remuneracao.total_liquido
        ).join(Remuneracao
               ).order_by(desc(Remuneracao.total_liquido)
                          )
        result = session.execute(stmt).mappings().all()
        result_dicts = [dict(row) for row in result]

    return jsonify(result_dicts)

@app.route("/diarias/valor-total")
def diarias_valor_total():
    with ORM() as db:
        session: Session = db.session

        stmt = select(
            Servidor.nome,
            func.sum(Diaria.valor_total).label("valor_total"),
            func.sum(Diaria.numero_diarias).label("num_diarias")
        ).join(Diaria
               ).group_by(Servidor.nome
                          ).order_by(desc("valor_total"))

        result = session.execute(stmt).mappings().all()
        result_dicts = [dict(row) for row in result]

    return jsonify(result_dicts)

@app.route("/indenizacoes/valor-total")
def indenizacoes_valor_total():
    with (ORM() as db):
        session: Session = db.session

        stmt = select(
            Servidor.nome,
            func.sum(VerbaIndenizatoria.total_pago).label("valor_total")
        ).join(VerbaIndenizatoria
               ).group_by(Servidor.nome
                          ).order_by(desc("valor_total")
                          )
        result = session.execute(stmt).mappings().all()
        result_dicts = [dict(row) for row in result]

    return jsonify(result_dicts)

@app.route("/indenizacoes")
def indenizacoes_por_tempo():
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')

    with (ORM() as db):
        session: Session = db.session

        stmt = select(
            VerbaIndenizatoria.data,
            func.sum(VerbaIndenizatoria.total_pago).label("valor_total")
        ).group_by(VerbaIndenizatoria.data
                  ).order_by(VerbaIndenizatoria.data
                            )
        result = session.execute(stmt).mappings().all()
        result_dicts = [dict(row) for row in result]

    return jsonify(result_dicts)


if __name__ == "__main__":
    # Porta configurada pela variável de ambiente ou padrão 4000
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)