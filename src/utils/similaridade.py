from rapidfuzz import process

from src.database.models import Servidor


def similaridade(session, nome_scraping):
    servidores = session.query(Servidor.id, Servidor.nome).all()
    nomes = [s.nome for s in servidores]

    best_match = process.extractOne(nome_scraping, nomes, score_cutoff=70)
    if best_match:
        nome, score, idx = best_match
        return servidores[idx].id
    return None