import datetime
import json
import os

from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.expression import select, desc, extract
from sqlalchemy.sql.functions import func

from src.database.models import Servidor, Remuneracao, Diaria, VerbaIndenizatoria, VerbaIndenizatoriaDetalhes

from src.database.orm import ORM
from datetime import date, datetime

app = Flask(__name__)
CORS(app)

@app.route("/salarios/total-liquido")
def salarios_total_liquido():
    nome = request.args.get('nome', '')
    maiorque = request.args.get('maiorque', 0.0)
    maiorque = 0.0 if maiorque == '' else float(maiorque)
    mes = int(request.args.get('mes', date.today().month))
    ano = int(request.args.get('ano', date.today().year))

    with ORM() as db:
        session: Session = db.session
        stmt = select(
            Servidor.nome,
            Remuneracao.total_liquido,
            Remuneracao.data
        ).join(Remuneracao
               ).where(
            Servidor.nome.like('%{}%'.format(nome)),
            Remuneracao.total_liquido > maiorque,
            extract("year", Remuneracao.data) == ano,
            extract("month", Remuneracao.data) == mes
                        ).group_by(Remuneracao.data
                        ).order_by(desc(Remuneracao.total_liquido)
                          )
        result = session.execute(stmt).mappings().all()
        result_dicts = [dict(row) for row in result]

    return jsonify(result_dicts)

@app.route("/diarias/valor-total")
def diarias_valor_total():
    nome = request.args.get('nome', '')
    maiorque = request.args.get('maiorque', 0.0)
    maiorque = 0.0 if maiorque == '' else float(maiorque)

    with ORM() as db:
        session: Session = db.session
        soma_total = func.sum(Diaria.valor_total)
        soma_diarias = func.sum(Diaria.numero_diarias)
        stmt = select(
            Servidor.nome,
            soma_total.label("valor_total"),
            soma_diarias.label("num_diarias")
        ).join(Diaria
               ).where(
            Servidor.nome.like('%{}%'.format(nome)),
        ).group_by(Servidor.nome
                          ).having(soma_total > maiorque
                                   ).order_by(desc("valor_total"))

        result = session.execute(stmt).mappings().all()
        result_dicts = [dict(row) for row in result]

    return jsonify(result_dicts)

@app.route("/indenizacoes/valor-total")
def indenizacoes_valor_total():
    nome = request.args.get('nome', '')
    maiorque = request.args.get('maiorque', 0.0)
    maiorque = 0.0 if maiorque == '' else float(maiorque)
    with ORM() as db:
        session: Session = db.session
        soma_total = func.sum(VerbaIndenizatoria.total_pago)

        stmt = select(
            Servidor.nome,
            soma_total.label("valor_total")
        ).join(VerbaIndenizatoria
               ).where(
            Servidor.nome.like('%{}%'.format(nome))
        ).group_by(Servidor.nome
                          ).having(soma_total > maiorque
        ).order_by(desc("valor_total")
                          )
        result = session.execute(stmt).mappings().all()
        result_dicts = [dict(row) for row in result]

    return jsonify(result_dicts)

@app.route("/indenizacoes/total-tempo")
def indenizacoes_por_tempo():
    data_inicio = request.args.get('dt_inicio', None)
    data_fim= request.args.get('dt_fim', None)
    maiorque = request.args.get('maiorque', 0.0)
    maiorque = 0.0 if maiorque == '' else float(maiorque)

    filtros = [

    ]

    if data_inicio:
        data_inicio = datetime.strptime(data_inicio, "%Y-%m-%d")
        filtros.append(VerbaIndenizatoria.data >= data_inicio)

    if data_fim:
        data_fim = datetime.strptime(data_fim, "%Y-%m-%d")
        filtros.append(VerbaIndenizatoria.data <= data_fim)



    with (ORM() as db):
        session: Session = db.session
        soma_total = func.sum(VerbaIndenizatoria.total_pago)

        stmt = select(
            VerbaIndenizatoria.data,
            soma_total.label("valor_total")
        ).where(
            *filtros
        ).group_by(VerbaIndenizatoria.data
                  ).having( soma_total > maiorque
        ).order_by(VerbaIndenizatoria.data
                            )
        result = session.execute(stmt).mappings().all()
        result_dicts = [dict(row) for row in result]

    return jsonify(result_dicts)

@app.route("/indenizacoes")
def indenizacoes():
    nome = request.args.get('nome', '')
    data = request.args.get('data')
    maiorque = request.args.get('maiorque', 0.0)
    maiorque = 0.0 if maiorque == '' else float(maiorque)
    data = datetime.strptime(data, "%Y-%m") if data else None

    filtros = [
        Servidor.nome.like('%{}%'.format(nome)),
        VerbaIndenizatoria.total_pago > maiorque,
    ]

    if data:
        filtros.extend(
           [
               extract("year", VerbaIndenizatoria.data) == data.year,
                extract("month", VerbaIndenizatoria.data) == data.month
           ]
        )





    with (ORM() as db):
        session: Session = db.session

        stmt = select(
            VerbaIndenizatoria.id,
            VerbaIndenizatoria.data,
            VerbaIndenizatoria.total_pago,
            Servidor.nome,
            VerbaIndenizatoriaDetalhes.classe.label("classe_servico"),
            VerbaIndenizatoriaDetalhes.prestador,
            VerbaIndenizatoriaDetalhes.data.label("data_servico"),
            VerbaIndenizatoriaDetalhes.valor

        ).join(
            Servidor
        ).join(
            VerbaIndenizatoriaDetalhes
        ).where(
            *filtros
        ).order_by(VerbaIndenizatoria.id
        )
        result = session.execute(stmt).mappings().all()
        result_dicts = [dict(row) for row in result]

    return jsonify(result_dicts)



if __name__ == "__main__":
    # Porta configurada pela variável de ambiente ou padrão 4000
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)