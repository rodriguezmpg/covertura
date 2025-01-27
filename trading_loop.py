
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
        self.input_sl = 0.00
        self.limite_inferior = 0.00
        self.contador = 0
        self.valor_steps = 0
        self.input_niveles = 0
        self.dist_perc = 0.00
        self.input_sloption = 0

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

lp = LoopData()


def process(msg):
    lp.current_price = float(msg['c'])  # 'c' es el precio actual del ticker
    if lp.current_price != lp.previous_price:
        lp.previous_price = lp.current_price
        print(f"Precio: {lp.current_price}  - Precio banda {lp.current_price}") 

        lp.contador = lp.contador + 1  #contador de envios del websocket

        if lp.input_sloption == 1:
            lp.percentsl = lp.input_sl
            lp.limite_inferior = lp.precio_banda - (lp.precio_banda*(lp.percentsl/100))
        else:
            lp.limite_inferior = lp.input_sl
            lp.percentsl = (1-(lp.limite_inferior/lp.precio_banda))*100

        lp.dist_perc = (lp.precio_banda - lp.limite_inferior) / lp.precio_banda
        lp.valor_steps = lp.dist_perc / lp.input_niveles

        lp.Po1_valor  = lp.precio_banda - (lp.precio_banda * (lp.valor_steps/2))
        lp.Po2_valor = lp.Po1_valor - (lp.precio_banda * lp.valor_steps)
        lp.Po3_valor = lp.Po2_valor - (lp.precio_banda * lp.valor_steps)
        lp.Po4_valor = lp.Po3_valor - (lp.precio_banda * lp.valor_steps)
        lp.Po5_valor = lp.Po4_valor - (lp.precio_banda * lp.valor_steps)
        lp.Po6_valor = lp.Po5_valor - (lp.precio_banda * lp.valor_steps)
        lp.Po7_valor = lp.Po6_valor - (lp.precio_banda * lp.valor_steps)

        lp.step1_valor = lp.precio_banda - (lp.precio_banda * lp.valor_steps)
        lp.step2_valor = lp.step1_valor - (lp.precio_banda * lp.valor_steps)
        lp.step3_valor = lp.step2_valor - (lp.precio_banda * lp.valor_steps)
        lp.step4_valor = lp.step3_valor - (lp.precio_banda * lp.valor_steps)
        lp.step5_valor = lp.step4_valor - (lp.precio_banda * lp.valor_steps)
        lp.step6_valor = lp.step5_valor - (lp.precio_banda * lp.valor_steps)


        if lp.current_price < lp.Po1_valor and not lp.control_posicion1: #E1
            lp.control_posicion1 = True
            lp.control_TP1 = True
        
        if lp.current_price <= lp.step1_valor and lp.control_TP1: #TP1
            lp.control_TP1 = False
            lp.contador_secuencia = 0

        if lp.current_price >= lp.precio_banda and lp.control_posicion1: #SL1
            lp.control_posicion1 = False
            if lp.control_TP1:
                lp.contador_secuencia = lp.contador_secuencia + 1
                lp.control_TP1 = False




async def start_socket(precio_banda_post, niveles_post_form, sl_post_form, sloption_post_form):
    bsm = BinanceSocketManager(client)
    socket = bsm.symbol_ticker_socket(symbol)
    lp.precio_banda = float(precio_banda_post)
    lp.input_niveles = int(niveles_post_form)
    lp.input_sloption  = int(sloption_post_form)
    lp.input_sl = float(sl_post_form)


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
           
         
                
