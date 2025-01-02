
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
        self.percentsl = 0.00
        self.limite_inferior = 0.00
        self.contador = 0
        self.valor_steps = 0
        self.input_niveles = 0
        self.dist_perc = 0.00

        self.contador_secuencia = 0

        self.Po1_valor = 0.00
        self.Po2_valor = 0.00
        self.Po3_valor = 0.00
        self.Po4_valor = 0.00
        self.Po5_valor = 0.00
        self.Po6_valor = 0.00
        self.Po7_valor = 0.00

        self.step1_valor = 0.00
        self.step2_valor = 0.00
        self.step3_valor = 0.00
        self.step4_valor = 0.00
        self.step5_valor = 0.00
        self.step6_valor = 0.00

        self.control_posicion1 = False
        self.control_posicion2 = False
        self.control_posicion3 = False
        self.control_posicion4 = False
        self.control_posicion5 = False
        self.control_posicion6 = False
        self.control_posicion7 = False

        self.control_TP1 = False
        self.control_TP2 = False
        self.control_TP3 = False
        self.control_TP4 = False
        self.control_TP5 = False
        self.control_TP6 = False
        self.control_TP7 = False


loop_class = LoopData()


def process(msg):
    loop_class.current_price = float(msg['c'])  # 'c' es el precio actual del ticker
    if loop_class.current_price != loop_class.previous_price:
        loop_class.previous_price = loop_class.current_price
        print(f"Precio: {loop_class.current_price}  - Precio banda {loop_class.current_price}") 

        loop_class.contador = loop_class.contador + 1  #contador de envios del websocket

    
        loop_class.limite_inferior = loop_class.precio_banda - (loop_class.precio_banda*(loop_class.percentsl/100))
        loop_class.dist_perc = (loop_class.precio_banda - loop_class.limite_inferior) / loop_class.precio_banda
        loop_class.valor_steps = loop_class.dist_perc / loop_class.input_niveles

        loop_class.Po1_valor  = loop_class.precio_banda - (loop_class.precio_banda * (loop_class.valor_steps/2))
        loop_class.Po2_valor = loop_class.Po1_valor - (loop_class.precio_banda * loop_class.valor_steps)
        loop_class.Po3_valor = loop_class.Po2_valor - (loop_class.precio_banda * loop_class.valor_steps)
        loop_class.Po4_valor = loop_class.Po3_valor - (loop_class.precio_banda * loop_class.valor_steps)
        loop_class.Po5_valor = loop_class.Po4_valor - (loop_class.precio_banda * loop_class.valor_steps)
        loop_class.Po6_valor = loop_class.Po5_valor - (loop_class.precio_banda * loop_class.valor_steps)
        loop_class.Po7_valor = loop_class.Po6_valor - (loop_class.precio_banda * loop_class.valor_steps)

        loop_class.step1_valor = loop_class.precio_banda - (loop_class.precio_banda * loop_class.valor_steps)
        loop_class.step2_valor = loop_class.step1_valor - (loop_class.precio_banda * loop_class.valor_steps)
        loop_class.step3_valor = loop_class.step2_valor - (loop_class.precio_banda * loop_class.valor_steps)
        loop_class.step4_valor = loop_class.step3_valor - (loop_class.precio_banda * loop_class.valor_steps)
        loop_class.step5_valor = loop_class.step4_valor - (loop_class.precio_banda * loop_class.valor_steps)
        loop_class.step6_valor = loop_class.step5_valor - (loop_class.precio_banda * loop_class.valor_steps)


        if loop_class.current_price < loop_class.Po1_valor and not loop_class.control_posicion1: #E1
            loop_class.control_posicion1 = True
            loop_class.control_TP1 = True
        
        if loop_class.current_price <= loop_class.step1_valor and loop_class.control_TP1: #TP1
            loop_class.control_TP1 = False
            loop_class.contador_secuencia = 0

        if loop_class.current_price >= loop_class.precio_banda and loop_class.control_posicion1: #SL1
            loop_class.control_posicion1 = False
            if loop_class.control_TP1:
                loop_class.contador_secuencia = loop_class.contador_secuencia + 1
                loop_class.control_TP1 = False




async def start_socket(precio_banda_post, niveles_post_form, percentsl_post_form):
    bsm = BinanceSocketManager(client)
    socket = bsm.symbol_ticker_socket(symbol)
    loop_class.precio_banda = float(precio_banda_post)
    loop_class.percentsl = float(percentsl_post_form)
    loop_class.input_niveles = int(niveles_post_form)


    async with socket as s:
        while True:
            msg = await s.recv()  
            process(msg)



if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_socket())


# def crear_csv():
#     with open("static/datos.csv", mode='w', newline='', encoding='utf-8') as archivo:
#         pass  
#     print("Archivo CSV creado o vaciado exitosamente.")
# crear_csv()  





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
           
         
                
