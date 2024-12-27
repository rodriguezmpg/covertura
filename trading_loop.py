
from binance.client import Client
from binance.enums import *
import csv
from datetime import datetime
import time
import logging


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

def main_loop(pe_post,niveles_post,percent_sl_post):
    ticker = client.futures_symbol_ticker(symbol=symbol) 
    loop_class.precio_banda = float(ticker['price'])#para obtener el precio cuando entro
    
    with open('output.log', 'w'):
        pass
    logging.basicConfig(filename='output.log', level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s',datefmt='%Y-%m-%d %H:%M:%S')
    logging.getLogger('werkzeug').setLevel(logging.WARNING)
    logger = logging.getLogger()

    while True:
    
        ticker = client.futures_symbol_ticker(symbol=symbol)
        loop_class.current_price = float(ticker['price'])

        if loop_class.current_price != loop_class.previous_price:
            print(f"Precio: {loop_class.current_price} : {pe_post} :  : {niveles_post} :  : {percent_sl_post}  ")        
            logger.info(f"{loop_class.current_price:.2f}")
            loop_class.previous_price = loop_class.current_price


        time.sleep(0.2)


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
           
         
                