from datetime import date
from src.controllers.scrapy import verbas_indenizatorias

def save_verbas_indenizatorias():
    data = date.today()
    verbas_indenizatorias(data)

