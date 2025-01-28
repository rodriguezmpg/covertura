from binance.client import Client
from binance.enums import *

API_KEY = '5ucUUmRpHMuB4vZsNrSrVKKQDpWMQJ4el1dZFYZzJUpBZ70RQtT0OToZxenWHjhs'
API_SECRET = '1Up2nryNOL2LZle6AjaSBiMwiC7L1wudS0u6RB001o1Vu1LlIEXPwsyIr1yI29GS'

# Crear cliente de Binance
client = Client(API_KEY, API_SECRET, tld='com')
symbol = 'ETHUSDT'

# Función para abrir una orden
def open_order():
    try:
        orden = client.futures_create_order(
            symbol='ETHUSDT',           
            side=SIDE_SELL,              
            type=ORDER_TYPE_MARKET,     
            quantity=0.01              
        )
        print(f"Orden abierta exitosamente: {orden}")
        return orden  # Regresa la respuesta de la orden
    except Exception as e:
        print(f"Error al abrir la orden: {e}")
        return str(e)



