from rapidfuzz import process

from src.database.models import Servidor


def similaridade(session, nome_scraping):
    servidores = session.query(Servidor.id, Servidor.nome).all()
    nomes = [s.nome for s in servidores]
    mapping = {s.nome: s.id for s in servidores}  # nome -> id

    best_match = process.extractOne(
        nome_scraping,
        nomes,
        score_cutoff=90
    )
    if best_match:
        nome, score, _ = best_match
        return mapping[nome]
    return None