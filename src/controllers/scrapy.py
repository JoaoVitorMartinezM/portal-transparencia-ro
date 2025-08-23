import re
from datetime import date, datetime
from os import environ

from bs4 import BeautifulSoup

from src.database.models import Servidor, VerbaIndenizatoria, VerbaIndenizatoriaDetalhes
from src.database.orm import ORM
from sqlalchemy.orm import Session
from os import environ

from src.utils.similaridade import similaridade


def verbas_indenizatorias(data: date):
    BASE_URL = environ['BASE_URL']
    PATH = environ['VERBAS_INDENIZATORIAS_PATH']

    params = {
        'gabinete': '',
        'categoria':'',
        'ano': data.year,
        'mes': data.month
    }
    url = BASE_URL + PATH
    soup = request_bsoup(url, params)

    linhas = soup.find_all("tr")

    with ORM() as db:

        ultimo_id = None
        for l in linhas:
            session: Session = db.session
            if len(l.get_text()) < 3:
                print("Pulou um vazio")
                continue

            if l.h4:
                texto = l.h4.get_text()
                padrao = re.compile(
                    r"(Deputad[oa](?: [^\-]+)?) - Mes: (?P<data>\d{1,2}/\d{4}) - Lote: (?P<lote>.*?) - Total pago: R\$ (?P<valor>[\d\.\,]+)"
                )
                match = padrao.search(texto)
                if match:
                    nome = match.group(1)
                    mes, ano = match.group("data").split("/")
                    lote = match.group("lote")
                    total_pago = float(match.group("valor").replace(".", "").replace(",", "."))
                    data = date(day=1, month=int(mes), year=int(ano))

                    # servidor_db = session.query(Servidor).filter(Servidor.nome == nome).first()
                    id_servidor = similaridade(session, nome)
                    if not id_servidor:
                        novo_servidor = Servidor(nome=nome)
                        session.add(novo_servidor)
                        session.flush()
                        id_servidor = novo_servidor.id

                    verba_db = session.query(VerbaIndenizatoria
                                  ).filter(VerbaIndenizatoria.id_servidor == id_servidor,
                                           VerbaIndenizatoria.data == data,
                                           VerbaIndenizatoria.total_pago == total_pago
                                           ).first()
                    if not verba_db:
                        verba_db = VerbaIndenizatoria(id_servidor=id_servidor, data=data, lote=lote, total_pago=total_pago)
                        session.add(verba_db)
                        session.commit()

                    ultimo_id = verba_db.id






                #Salva verba e guarda id depois do commit
                # print(saida)

            if l.td and not l.td.h4:
                #Salva detalhes para o ultimo verba id cadastrado
                texto = l.td.get_text()
                padrao = re.compile(
                    r"Prestador: (?P<prestador>.*?)\|"
                    r"\s*Classe: (?P<classe>.*?)\|"
                    r"\s*Data: (?P<data>\d{2}/\d{2}/\d{4})\s*\|"
                    r"\s*Valor: R\$ (?P<valor>[\d\.\,]+)"
                )

                match = padrao.search(texto)
                if match:
                    prestador = match.group("prestador").strip()
                    classe = match.group("classe").strip()
                    dia, mes, ano = match.group("data").split("/")
                    data = date(day=int(dia), month=int(mes), year=int(ano))
                    valor_str = match.group("valor").replace(".", "").replace(",", ".")
                    valor = float(valor_str)

                    verba_detalhes_db = session.query(VerbaIndenizatoriaDetalhes
                                  ).filter(
                        VerbaIndenizatoriaDetalhes.id_verba_indenizatoria == ultimo_id,
                        VerbaIndenizatoriaDetalhes.data == data,
                        VerbaIndenizatoriaDetalhes.valor == valor
                    ).first()

                    if not verba_detalhes_db:
                        verba_detalhes_model = VerbaIndenizatoriaDetalhes(prestador=prestador, classe=classe,data=data, valor=valor, id_verba_indenizatoria=ultimo_id)
                        session.add(verba_detalhes_model)
                        session.commit()

def diarias_deputados(data: date):
    BASE_URL = environ['BASE_URL']
    PATH = environ['DIARIAS_PATH']
    url = BASE_URL + PATH

    params = {
        'nome': '',
        'ano': data.year,
        'mes': data.month
    }

    soup = request_bsoup(url, params)
    tabela = soup.find_all("table")[1]
    informacoes_list = tabela.find_all("a")

    def extrai_detalhes_id(item):
        href = item["href"]
        id = href.split("/")[-1]
        return id

    detalhes_ids = list(map(extrai_detalhes_id, informacoes_list))
    diarias_list = []
    for id in detalhes_ids:
        path = environ['DIARIAS_DETALHES_PATH']
        url = BASE_URL + path + id
        soup = request_bsoup(url)
        divs = soup.find_all(class_="conteudo-documento-linha")
        diaria = {}
        deputado = soup.find(class_="conteudo-documento-cabecalho-texto").get_text()
        diaria["Deputado"] = deputado
        for div in divs:
            if div.get_text().strip() in ["", "Tipo Veículo", "Ordem Bancária", "Empenho"]:
                continue
            campo = div.get_text().strip().split('\n')
            lista = list(filter(lambda x: x != '', map(lambda x: x.strip(), campo)))
            chave, valor = div.get_text().strip().split('\n', 1)
            diaria[chave] = valor.replace("\n", "").strip()

        diaria["Total"] = diaria["Total"].replace(".", "").replace(",", ".").replace("R$ ", "")
        diaria["Total"] = float(diaria["Total"])
        diaria["Valor Unitário"] = diaria["Valor Unitário"].replace(".", "").replace(",", ".").replace("R$ ", "")
        diaria["Valor Unitário"] = float(diaria["Valor Unitário"])

        dia, mes, ano = diaria["Dt. Saída"].split("/")
        diaria["Dt. Saída"] = datetime(day=int(dia), month=int(mes), year=int(ano))


        diarias_list.append(diaria)

    return diarias_list

def remuneracao_deputados(data:date):

    BASE_URL = environ['BASE_URL']
    PATH = environ['REMUNERACAO_PATH']
    url = BASE_URL + PATH

    params = {
        'ano': data.year,
        'mes': data.month
    }

    resp = get(url, params=params)

    if resp.status_code != 200:
        raise Exception(f'A requisição para {url} falhou.')

    print(f'Acesso em {url}')
    return resp.json()



def request_bsoup(url, params=None):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Referer": "https://www.google.com"
    }

    resp = get(url, headers=headers, params=params)

    if resp.status_code != 200:
        raise Exception(f'A requisição para {url} falhou.')

    print(f'Acesso em {url}')
    soup = BeautifulSoup(resp.content, "html.parser")
    return soup

from requests import get