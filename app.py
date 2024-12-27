from flask import Flask
from binance.client import Client
from binance.enums import *

app = Flask(__name__)

APY_KEY = 'pYBw0fO0OisuqFXhwj2SNy2DYU8N1MFCH2zJ2CUeYGiHwCa7DazkOjCChJaMfyth'
APY_SECRET = 'EdPJTJn5gnCSgq3HpuuNANPLRHwtTA7TZLIp5Mb8aLIFjqyYCjjDDuXVDcLbyC2i'

client = Client(APY_KEY,APY_SECRET, tld='com')
symbol = 'ETHUSDT'

@app.route('/')
def hello():
    # Obtener el precio de ETH/USDT
    try:
        eth_price = client.get_symbol_ticker(symbol="ETHUSDT")
        return f"El precio actual de ETH/USDT es: {eth_price['price']}"
    except Exception as e:
        return f"Ocurrió un error al obtener el precio: {str(e)}"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
