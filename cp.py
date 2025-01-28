from binance.client import Client
from binance.enums import *


APY_KEY = '5ucUUmRpHMuB4vZsNrSrVKKQDpWMQJ4el1dZFYZzJUpBZ70RQtT0OToZxenWHjhs'
APY_SECRET = '1Up2nryNOL2LZle6AjaSBiMwiC7L1wudS0u6RB001o1Vu1LlIEXPwsyIr1yI29GS'

client = Client(APY_KEY,APY_SECRET, tld='com')
symbol = 'ETHUSDT'

def open_order():
    orden = client.futures_create_order(
        symbol='ETHUSDT',           
        side=SIDE_SELL,              
        type=ORDER_TYPE_MARKET,     
        quantity=0.01              
    )
    print(f"Orden abierta exitosamente: {orden}")
    return jsonify(order)


