import datetime
import os
from tokenize import group

from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.expression import select, desc, extract
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.selectable import Select

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
    mes = request.args.get('mes', None)
    ano = request.args.get('ano', None)
    data_inicio = request.args.get('dt_inicio', None)
    data_fim= request.args.get('dt_fim', None)
    order_by = request.args.get('order_by', "data")
    group_by = request.args.get('group_by', "data")

    filtros = [
        Servidor.nome.like('%{}%'.format(nome)),
        Remuneracao.total_liquido > maiorque
    ]
    if ano:
        ano = int(ano)
        filtros.append(extract("year", Remuneracao.data) == ano)
    if mes:
        mes =int(mes)
        filtros.append(extract("month", Remuneracao.data) == mes)

    if data_inicio:
        data_inicio = datetime.strptime(data_inicio, "%m-%Y")
        filtros.append(Remuneracao.data >= data_inicio)

    if data_fim:
        data_fim = datetime.strptime(data_fim, "%m-%Y")
        filtros.append(Remuneracao.data <= data_fim)


    with ORM() as db:
        session: Session = db.session
        columns: list = [Servidor.nome]
        soma_total_liquido = func.sum(Remuneracao.total_liquido).label("total_liquido")
        stmt: Select


        if group_by.__eq__("data"):
            columns.extend([Remuneracao.data, Remuneracao.total_liquido])
            stmt = select(*columns).join(Remuneracao).where(*filtros)
        else:
            columns.append(soma_total_liquido)
            stmt = select(*columns).join(Remuneracao).where(*filtros).group_by(Servidor.nome)

        if order_by.__eq__("data"):
            stmt = stmt.order_by(Remuneracao.data)
        else:
            stmt = stmt.order_by(desc("total_liquido"))

        result = session.execute(stmt).mappings().all()
        result_dicts = [dict(row) for row in result]

    return jsonify(result_dicts)

@app.route("/diarias/valor-total")
def diarias_valor_total():
    nome = request.args.get('nome', '')
    maiorque = request.args.get('maiorque', 0.0)
    maiorque = 0.0 if maiorque == '' else float(maiorque)
    data_inicio = request.args.get('dt_inicio', None)
    data_fim = request.args.get('dt_fim', None)

    with ORM() as db:
        session: Session = db.session
        soma_total = func.sum(Diaria.valor_total)
        soma_diarias = func.sum(Diaria.numero_diarias)

        filtros = [
            Servidor.nome.like('%{}%'.format(nome)),
        ]

        if data_inicio:
            data_inicio = datetime.strptime(data_inicio, "%m-%Y")
            filtros.append(VerbaIndenizatoria.data >= data_inicio)
        if data_fim:
            data_fim = datetime.strptime(data_fim, "%m-%Y")
            filtros.append(VerbaIndenizatoria.data <= data_fim)

        stmt = select(
            Servidor.nome,
            soma_total.label("valor_total"),
            soma_diarias.label("num_diarias")
        ).join(Diaria
               ).where(
            *filtros
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
    data_inicio = request.args.get('dt_inicio', None)
    data_fim= request.args.get('dt_fim', None)


    with ORM() as db:
        session: Session = db.session
        soma_total = func.sum(VerbaIndenizatoria.total_pago)

        filtros = [
            Servidor.nome.like('%{}%'.format(nome))
        ]

        if data_inicio:
            data_inicio = datetime.strptime(data_inicio, "%m-%Y")
            filtros.append(VerbaIndenizatoria.data >= data_inicio)
        if data_fim:
            data_fim = datetime.strptime(data_fim, "%m-%Y")
            filtros.append(VerbaIndenizatoria.data <= data_fim)

        stmt = select(
            Servidor.nome,
            soma_total.label("valor_total")
        ).join(VerbaIndenizatoria
               ).where(
            *filtros
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
        data_inicio = datetime.strptime(data_inicio, "%m-%Y")
        filtros.append(VerbaIndenizatoria.data >= data_inicio)

    if data_fim:
        data_fim = datetime.strptime(data_fim, "%m-%Y")
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
    data = datetime.strptime(data, "%m-%Y") if data else None

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