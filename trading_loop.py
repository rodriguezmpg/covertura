
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
    try:
        loop_class.current_price = float(msg['c'])  # 'c' es el precio actual del ticker
        if loop_class.current_price != loop_class.previous_price:
            # Aquí simulas la impresión que hacías antes en la consola
            print(f"Precio: {loop_class.current_price} ")        
            # También logueas el precio
            logger.info(f"{loop_class.current_price:.2f}")
            loop_class.previous_price = loop_class.current_price
    except Exception as e:
        logger.error(f"Error al procesar el mensaje: {str(e)}")

# Función para iniciar el WebSocket y escuchar el precio en tiempo real
async def main():
    # Crear un socket para el precio de ETHUSDT
    bsm = BinanceSocketManager(client)
    socket = bsm.symbol_ticker_socket(symbol)

    # Comienza a escuchar los mensajes del socket
    async with socket as s:
        while True:
            msg = await s.recv()  # Recibe el mensaje del WebSocket
            process_message(msg)

# Función principal que ejecuta el loop de WebSocket
if __name__ == '__main__':
    logging.basicConfig(filename='output.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    logging.getLogger('werkzeug').setLevel(logging.WARNING)
    logger = logging.getLogger()

    # Iniciar el loop asincrónico de WebSocket
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())


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
           
         
                
