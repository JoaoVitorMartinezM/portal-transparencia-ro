from requests import get
from os import environ

def get_servidores():
    SERVIDORES_URL = environ['SERVIDORES_URL']
    try:
        data = get(SERVIDORES_URL)
        return data.json()
    except:
        return []