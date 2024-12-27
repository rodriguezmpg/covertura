from flask import Flask
from binance.client import Client
from binance.enums import *

app = Flask(__name__)

APY_KEY = 'pYBw0fO0OisuqFXhwj2SNy2DYU8N1MFCH2zJ2CUeYGiHwCa7DazkOjCChJaMfyth'
APY_SECRET = 'EdPJTJn5gnCSgq3HpuuNANPLRHwtTA7TZLIp5Mb8aLIFjqyYCjjDDuXVDcLbyC2i'

client = Client(APY_KEY,APY_SECRET, tld='com')
symbol = 'ETHUSDT'


@app.route('/')
def get_eth_price():
    try:
        # Obtener el precio actual de ETH/USDT
        ticker = client.get_symbol_ticker(symbol="ETHUSDT")
        eth_price = ticker['price']  # Extraer el precio de la respuesta
        return f"El precio actual de ETH/USDT es: ${eth_price}"
    except Exception as e:
        # En caso de error, mostrar el mensaje de error
        return f"Error al obtener el precio de ETH/USDT: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
