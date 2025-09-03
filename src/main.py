from src.database.models import Servidor
from src.database.orm import ORM
from dotenv import load_dotenv
from src.services import get_servidores, save_servidores, save_verbas_indenizatorias, save_diarias, save_remuneracoes

load_dotenv()
orm = ORM()
orm.generateBD()

# Consulta os servidores públicos da API
servidores = get_servidores()

# Salva os servidores públicos no banco de dados
save_servidores(servidores)
save_verbas_indenizatorias()
save_diarias()
save_remuneracoes()





