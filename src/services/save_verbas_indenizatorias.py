from datetime import date
from src.controllers.scrapy import verbas_indenizatorias

def save_verbas_indenizatorias():
    data = date(day=1, month=6, year=2025)

    verbas_indenizatorias(data)

