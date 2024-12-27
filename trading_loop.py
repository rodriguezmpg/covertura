
from binance.client import Client
from binance.enums import *
from binance.streams import BinanceSocketManager
import csv
from datetime import datetime
import time
import logging
import asyncio


APY_KEY = 'pYBw0fO0OisuqFXhwj2SNy2DYU8N1MFCH2zJ2CUeYGiHwCa7DazkOjCChJaMfyth'
APY_SECRET = 'EdPJTJn5gnCSgq3HpuuNANPLRHwtTA7TZLIp5Mb8aLIFjqyYCjjDDuXVDcLbyC2i'

client = Client(APY_KEY,APY_SECRET, tld='com')
symbol = 'ETHUSDT'


class LoopData:
    def __init__(self):
        self.precio_banda = 0.00
        self.current_price = 0.00
        self.previous_price = 0.00

loop_class = LoopData()

# Función para procesar los mensajes del WebSocket
def process_message(msg):
    loop_class.current_price = float(msg['c'])  # 'c' es el precio actual del ticker
    if loop_class.current_price != loop_class.previous_price:
        print(f"Precio: {loop_class.current_price}  - Precio banda {loop_class.current_price}")        
        loop_class.previous_price = loop_class.current_price


async def start_socket(precio_banda_post, niveles_post_form, percentsl_post_form):
    bsm = BinanceSocketManager(client)
    socket = bsm.symbol_ticker_socket(symbol)
    loop_class.precio_banda = precio_banda_post


    async with socket as s:
        while True:
            msg = await s.recv()  
            process_message(msg)



if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_socket())


def crear_csv():
    with open("static/datos.csv", mode='w', newline='', encoding='utf-8') as archivo:
        pass  
    print("Archivo CSV creado o vaciado exitosamente.")
crear_csv()  








     # ######################### DATOS CSV ############################
            # datos = [
            #             [
            #             contador_posiciones, 
            #             precioentrada, 
            #             preciosalida, 
            #             f"{pnl_sl:.2f}",
            #             f"{dif_porcentual * 100:.5f}",
            #             f"{control_tp}",
            #             f"{pnl_tp:.2f}",
            #             f"{tp_short:.2f}",
            #             f"{precio_tp:.2f}",
            #             fecha_hora_op,
            #             fecha_hora_cl
                        
                    
            #             ]
            #         ]
            
            
            # with open("app/static/datos.csv", mode='a', newline='', encoding='utf-8') as archivo: 
            #     escritor_csv = csv.writer(archivo)
            #     escritor_csv.writerows(datos)
            # ######################### FIN DATOS CSV ############################
           
         
                
