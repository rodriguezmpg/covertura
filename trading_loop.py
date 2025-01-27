
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


class LoopData: ##VARIABLES UTILIZADAS EN LA SIMULACION
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
        self.capital_base = 0.00
        self.Qty_PosicionTotal = 0.00 #Tamanio total de la posicion a cubrir
        self.valor_SubSL = 0.00
        self.perc_SubSL = 0.00

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

        self.recorrido_perc1 = 0.00
        self.recorrido_perc2 = 0.00
        self.recorrido_perc3 = 0.00
        self.recorrido_perc4 = 0.00
        self.recorrido_perc5 = 0.00
        self.recorrido_perc6 = 0.00
        self.recorrido_perc7 = 0.00
        self.sum_recorrrido_perc = 0.00

        self.PF_esperado1 = 0.00
        self.PF_esperado2 = 0.00
        self.PF_esperado3 = 0.00
        self.PF_esperado4 = 0.00
        self.PF_esperado5 = 0.00
        self.PF_esperado6 = 0.00
        self.PF_esperado7 = 0.00
        self.sum_PF_esperado = 0.00

        self.Qty_USDT_SubPosicion = 0.00
        self.sum_Qty_USDT_SubPosicion = 0.00

        self.Qty_mVar1 = 0.000
        self.Qty_mVar2 = 0.000
        self.Qty_mVar3 = 0.000
        self.Qty_mVar4 = 0.000
        self.Qty_mVar5 = 0.000
        self.Qty_mVar6 = 0.000
        self.Qty_mVar7 = 0.000
        self.sum_Qty_mVar = 0.000

        self.T4_valorperdida = 0.00
        self.T5_valorperdida = 0.00
        self.T6_valorperdida = 0.00
        self.T4_percperdida = 0.00
        self.T5_percperdida = 0.00
        self.T6_percperdida = 0.00
        self.T4_MaxUSDTQty = 0.00
        self.T5_MaxUSDTQty = 0.00
        self.T6_MaxUSDTQty = 0.00
        





        #variables de posiciones (capaz hacemos otra clase)
        self.control_pos1 = False
        self.control_pos2 = False
        self.control_pos3 = False
        self.control_pos4 = False
        self.control_pos5 = False
        self.control_pos6 = False
        self.control_pos7 = False

        self.control_TP1 = False
        self.control_TP2 = False
        self.control_TP3 = False
        self.control_TP4 = False
        self.control_TP5 = False
        self.control_TP6 = False
        self.control_TP7 = False

        
lp = LoopData()


def calculos(msg):
    lp.current_price = float(msg['c'])  # 'c' es el precio actual del ticker
    if lp.current_price != lp.previous_price:
        lp.previous_price = lp.current_price
        print(f"Precio: {lp.current_price}  - Precio banda {lp.current_price}") 

        lp.contador = lp.contador + 1  #contador de envios del websocket

        ## DEFINE EL SL EN BASE A SI ES % O SI ES UN VALOR
        if lp.input_sloption == 1:
            lp.percentsl = lp.input_sl
            lp.limite_inferior = lp.precio_banda - (lp.precio_banda*(lp.percentsl/100))
        else:
            lp.limite_inferior = lp.input_sl
            lp.percentsl = (1-(lp.limite_inferior/lp.precio_banda))*100

        lp.dist_perc = (lp.precio_banda - lp.limite_inferior) / lp.precio_banda #Distancia porcentual total
        lp.valor_steps = lp.dist_perc / lp.input_niveles #Valor porcentual de cada escalon

        lp.Po1_valor  = lp.precio_banda - (lp.precio_banda * (lp.valor_steps/2)) #Valores de apertura de posicion
        lp.Po2_valor = lp.Po1_valor - (lp.precio_banda * lp.valor_steps)
        lp.Po3_valor = lp.Po2_valor - (lp.precio_banda * lp.valor_steps)
        lp.Po4_valor = lp.Po3_valor - (lp.precio_banda * lp.valor_steps)
        lp.Po5_valor = lp.Po4_valor - (lp.precio_banda * lp.valor_steps)
        if lp.input_niveles > 5:
            lp.Po6_valor = lp.Po5_valor - (lp.precio_banda * lp.valor_steps)
            lp.Po7_valor = lp.Po6_valor - (lp.precio_banda * lp.valor_steps)

        lp.step1_valor = lp.precio_banda - (lp.precio_banda * lp.valor_steps) #Valores de TP y SL
        lp.step2_valor = lp.step1_valor - (lp.precio_banda * lp.valor_steps)
        lp.step3_valor = lp.step2_valor - (lp.precio_banda * lp.valor_steps)
        lp.step4_valor = lp.step3_valor - (lp.precio_banda * lp.valor_steps)
        lp.step5_valor = lp.step4_valor - (lp.precio_banda * lp.valor_steps)
        if lp.input_niveles > 5:lp.step6_valor = lp.step5_valor - (lp.precio_banda * lp.valor_steps)


        lp.recorrido_perc1 = (lp.Po1_valor - lp.limite_inferior) / lp.Po1_valor #Recorridos porcentuales
        lp.recorrido_perc2 = (lp.Po2_valor - lp.limite_inferior) / lp.Po2_valor
        lp.recorrido_perc3 = (lp.Po3_valor - lp.limite_inferior) / lp.Po3_valor
        lp.recorrido_perc4 = (lp.Po4_valor - lp.limite_inferior) / lp.Po4_valor
        lp.recorrido_perc5 = (lp.Po5_valor - lp.limite_inferior) / lp.Po5_valor
        if lp.input_niveles > 5:
            lp.recorrido_perc6 = (lp.Po6_valor - lp.limite_inferior) / lp.Po6_valor
            lp.recorrido_perc7 = (lp.Po7_valor - lp.limite_inferior) / lp.Po7_valor
        lp.sum_recorrrido_perc = lp.recorrido_perc1 + lp.recorrido_perc2 + lp.recorrido_perc3 + lp.recorrido_perc4 + lp.recorrido_perc5 + lp.recorrido_perc6 + lp.recorrido_perc7

        
        lp.Qty_PosicionTotal = (lp.capital_base * 5) / (lp.percentsl * 2) #Cual es el total de la posicion en base al capital base para que el SL este en 2,5% de perdida.
        lp.PF_esperado1 = (lp.recorrido_perc1 / lp.sum_recorrrido_perc) * (lp.Qty_PosicionTotal * (lp.percentsl/100)) #Calculo del profit esperado de cada SubPosicion
        lp.PF_esperado2 = (lp.recorrido_perc2 / lp.sum_recorrrido_perc) * (lp.Qty_PosicionTotal * (lp.percentsl/100))
        lp.PF_esperado3 = (lp.recorrido_perc3 / lp.sum_recorrrido_perc) * (lp.Qty_PosicionTotal * (lp.percentsl/100))
        lp.PF_esperado4 = (lp.recorrido_perc4 / lp.sum_recorrrido_perc) * (lp.Qty_PosicionTotal * (lp.percentsl/100))
        lp.PF_esperado5 = (lp.recorrido_perc5 / lp.sum_recorrrido_perc) * (lp.Qty_PosicionTotal * (lp.percentsl/100))
        if lp.input_niveles > 5:
            lp.PF_esperado6 = (lp.recorrido_perc6 / lp.sum_recorrrido_perc) * (lp.Qty_PosicionTotal * (lp.percentsl/100))
            lp.PF_esperado7 = (lp.recorrido_perc7 / lp.sum_recorrrido_perc) * (lp.Qty_PosicionTotal * (lp.percentsl/100))
        lp.sum_PF_esperado = lp.PF_esperado1 + lp.PF_esperado2 + lp.PF_esperado3 + lp.PF_esperado4 + lp.PF_esperado5 +lp.PF_esperado6 + lp.PF_esperado7

        lp.Qty_USDT_SubPosicion = lp.PF_esperado1 / lp.recorrido_perc1 #Cantidad de USDT de cada sub posicion
        if lp.input_niveles > 5:lp.sum_Qty_USDT_SubPosicion = lp.Qty_USDT_SubPosicion * 7
        else:lp.sum_Qty_USDT_SubPosicion = lp.Qty_USDT_SubPosicion * 5

        lp.Qty_mVar1 = lp.Qty_USDT_SubPosicion / lp.Po1_valor #Cantidad de moneda de cada sub posicion
        lp.Qty_mVar2 = lp.Qty_USDT_SubPosicion / lp.Po2_valor
        lp.Qty_mVar3 = lp.Qty_USDT_SubPosicion / lp.Po3_valor
        lp.Qty_mVar4 = lp.Qty_USDT_SubPosicion / lp.Po4_valor
        lp.Qty_mVar5 = lp.Qty_USDT_SubPosicion / lp.Po5_valor
        if lp.input_niveles > 5:
            lp.Qty_mVar6 = lp.Qty_USDT_SubPosicion / lp.Po6_valor
            lp.Qty_mVar7 = lp.Qty_USDT_SubPosicion / lp.Po7_valor
        lp.sum_Qty_mVar = lp.Qty_mVar1 + lp.Qty_mVar2 + lp.Qty_mVar3 + lp.Qty_mVar4 + lp.Qty_mVar5 + lp.Qty_mVar6 + lp.Qty_mVar7

        lp.perc_SubSL = (lp.percentsl / 100) / (lp.input_niveles * 2) #Distancia porcentual de PE y el SL de cada Sub Posicion
        lp.valor_SubSL = lp.perc_SubSL * lp.Qty_USDT_SubPosicion #Valor de perdida que me dara el SL de cada Sub Posicion
        
        lp.T4_valorperdida = lp.valor_SubSL * (2**4) #valor de la perdida en cada toque
        lp.T5_valorperdida = lp.valor_SubSL * (2**5)
        lp.T6_valorperdida = lp.valor_SubSL * (2**6)
        lp.T4_percperdida = lp.T4_valorperdida / lp.capital_base #porcentaje del capital total que representa la perdida en cada toque
        lp.T5_percperdida = lp.T5_valorperdida / lp.capital_base
        lp.T6_percperdida = lp.T6_valorperdida / lp.capital_base
        lp.T4_MaxUSDTQty = lp.T4_valorperdida / lp.perc_SubSL #Volumen de la posicion a abrir en ese toque
        lp.T5_MaxUSDTQty = lp.T5_valorperdida / lp.perc_SubSL
        lp.T6_MaxUSDTQty = lp.T6_valorperdida / lp.perc_SubSL



        #LOGICA DE POSICIONES

        if lp.current_price < lp.Po1_valor and not lp.control_pos1: #POS1
            lp.control_pos1 = True

        if lp.current_price < lp.step1_valor and not lp.control_TP1: #TP1
            lp.control_TP1 = True

        if lp.current_price > lp.precio_banda and lp.control_pos1: #SL1
            lp.control_pos1 = False

        
        






async def start_socket(precio_banda_post, niveles_post_form, sl_post_form, sloption_post_form):
    bsm = BinanceSocketManager(client)
    socket = bsm.symbol_ticker_socket(symbol)

    ## PASO LOS VALORES POST A LAS VARIABLES DE LA CLASE
    lp.precio_banda = float(precio_banda_post)
    lp.input_niveles = int(niveles_post_form)
    lp.input_sloption  = int(sloption_post_form)
    lp.input_sl = float(sl_post_form)
    lp.capital_base = 10000
    

    async with socket as s:
        while True:
            msg = await s.recv()  
            calculos(msg)



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
           
         
                
