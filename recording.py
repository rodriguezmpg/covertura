from binance.client import Client
import csv
from datetime import datetime
import time
import sqlite3


APY_KEY = 'pYBw0fO0OisuqFXhwj2SNy2DYU8N1MFCH2zJ2CUeYGiHwCa7DazkOjCChJaMfyth'
APY_SECRET = 'EdPJTJn5gnCSgq3HpuuNANPLRHwtTA7TZLIp5Mb8aLIFjqyYCjjDDuXVDcLbyC2i'

client = Client(APY_KEY, APY_SECRET, tld='com')

symbol = 'ETHUSDT'
previous_price = None
current_price = 0.00


ticker = client.futures_symbol_ticker(symbol=symbol)
current_price = float(ticker['price'])
timestamp = datetime.now().strftime('%m%d_%H%M')

db_file_path = f"static/backtest_files/{timestamp}_{current_price}.db"


def recording_loop():
    global ticker, current_price, previous_price

    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS precios (
                    timestamp TEXT,
                    price REAL
                )''')
    conn.commit()

    while True:
        ticker = client.futures_symbol_ticker(symbol=symbol)
        current_price = float(ticker['price'])

        if previous_price is None or current_price != previous_price:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute("INSERT INTO precios (timestamp, price) VALUES (?, ?)", (timestamp, current_price))
            conn.commit() 

        previous_price = current_price
        time.sleep(0.2)



# recording_loop() Si le activo esto funciona llamando directamente al programa y no llamandolo a traves de APP













