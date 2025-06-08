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

client = Client(APY_KEY,APY_SECRET, tld='com') #prueba de pus
symbol = 'ETHUSDT'



class FixedData: ##VARIABLES UTILIZADAS EN LA SIMULACION
    def __init__(self):
        self.precio_banda = 0.00 #ultimo intentode push
        self.current_price = 0.00
        self.previous_price = 0.00
        self.percentsl = 0.00 #es la distancia porcentual entre el PE y el limite inferior.
        self.input_sl = 0.00
        self.limite_inferior = 0.00
        self.contador = 0
        self.valor_steps = 0
        self.input_niveles = 0
        self.dist_perc = 0.00
        self.input_sloption = 0
        self.capital_base = 0.00
        self.Qty_PosicionTotal = 0.00 #Tamanio total de la posicion a cubrir

        self.valor_SubSL1 = 0.00
        self.perc_SubSL1 = 0.00

        self.Po_valor = [0.00] * 8
        self.step_valor = [0.00] * 7 #El maximo es el step 6
        self.recorrido_perc = [0.00] * 8 
        self.sum_recorrrido_perc = 0.00

        self.PF_esperado = [0.00] * 8

        self.sum_PF_esperado = 0.00

        self.Qty_USDT_SubPosicion = 0.00
        self.sum_Qty_USDT_SubPosicion = 0.00

        self.Qty_mVar = [0.000] * 8
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

lp = FixedData()


class RealTime: ##VARIABLES UTILIZADAS EN LAS POSICIONES
    def __init__(self):
        self.control_pos = [False] * 8
        self.control_TP = [False] * 8
     
        self.PE_Pos = [0.00] * 8
        self.TP_Pos = [0.00] * 8
        self.SL_Pos = [0.00] * 8

        self.Qty_USDT_SubPosicion = 0.00 

        self.Bal_Pos = [0.00] * 8

        self.PnL_SL = [0.00] * 8
        self.PnL_SL1_array = []
        self.Pnl_TP = [0.00] * 8

        self.Qty_mVar = [0.000] * 8
        self.Qty_mVar_rec = [0.000] * 8
        self.Qty_mVar_rec_acum = [0.000] * 8

        self.ValorPuro_Pos = [0.00] * 8

        self.PE_TP_Pos = [0.00] * 8
        self.PE_SL_Pos = [0.00] * 8 #Precio al que se ejecuto el TP
 
        self.cont_hits = [0] * 8  
 
rt = RealTime()

class WCSV: ##VARIABLES UTILIZADAS EN EL CSV
    def __init__(self):
        self.id_posicion = 0
        self.type_Pos = ""
wcsv = WCSV()

#Para borrar la simulacion solamente tengo que dejar lo que esta dentro del FOR
#    dentro de la funcion calculos() y recordar borrar el timesleep al ultimo

prices = [990,1000,990,1000,990,1000,990,1000,990,980,1000,989,979,999,989,978,1000,988,1000,988,1002,990,1000,990,980,920]

control_simulacion = True

def calculos(msg):
    global control_simulacion      
    if control_simulacion:        
        control_simulacion = False
        for price in prices:     
            lp.current_price = price  
            #lp.current_price = float(msg['c'])  # 'c' es el precio actual del ticker // Borrar donde puse en las variables post que es un POST
            if lp.current_price != lp.previous_price:
                lp.previous_price = lp.current_price
                print(f"Precio: {lp.current_price}") 

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

                lp.Po_valor[1]  = lp.precio_banda - (lp.precio_banda * (lp.valor_steps/2)) #Valores de apertura de posicion
                lp.Po_valor[2] = lp.Po_valor[1] - (lp.precio_banda * lp.valor_steps)
                lp.Po_valor[3] = lp.Po_valor[2] - (lp.precio_banda * lp.valor_steps)
                lp.Po_valor[4] = lp.Po_valor[3] - (lp.precio_banda * lp.valor_steps)
                lp.Po_valor[5] = lp.Po_valor[4] - (lp.precio_banda * lp.valor_steps)
                if lp.input_niveles > 5:
                    lp.Po_valor[6] = lp.Po_valor[5] - (lp.precio_banda * lp.valor_steps)
                    lp.Po_valor[7] = lp.Po_valor[6] - (lp.precio_banda * lp.valor_steps)

                lp.step_valor[1] = lp.precio_banda - (lp.precio_banda * lp.valor_steps) #Valores de TP y SL
                lp.step_valor[2] = lp.step_valor[1] - (lp.precio_banda * lp.valor_steps)
                lp.step_valor[3] = lp.step_valor[2] - (lp.precio_banda * lp.valor_steps)
                lp.step_valor[4] = lp.step_valor[3] - (lp.precio_banda * lp.valor_steps)
                lp.step_valor[5] = lp.step_valor[4] - (lp.precio_banda * lp.valor_steps)
                if lp.input_niveles > 5:lp.step_valor[6] = lp.step_valor[5] - (lp.precio_banda * lp.valor_steps)

                
                lp.recorrido_perc[1] = (lp.Po_valor[1] - lp.limite_inferior) / lp.Po_valor[1] #Recorridos porcentuales
                lp.recorrido_perc[2] = (lp.Po_valor[2] - lp.limite_inferior) / lp.Po_valor[2]
                lp.recorrido_perc[3] = (lp.Po_valor[3] - lp.limite_inferior) / lp.Po_valor[3]
                lp.recorrido_perc[4] = (lp.Po_valor[4] - lp.limite_inferior) / lp.Po_valor[4]
                lp.recorrido_perc[5] = (lp.Po_valor[5] - lp.limite_inferior) / lp.Po_valor[5]
                if lp.input_niveles > 5:
                    lp.recorrido_perc[6] = (lp.Po_valor[6] - lp.limite_inferior) / lp.Po_valor[6]
                    lp.recorrido_perc[7] = (lp.Po_valor[7] - lp.limite_inferior) / lp.Po_valor[7]
                lp.sum_recorrrido_perc = lp.recorrido_perc[1] + lp.recorrido_perc[2] + lp.recorrido_perc[3] + lp.recorrido_perc[4] + lp.recorrido_perc[5] + lp.recorrido_perc[6] + lp.recorrido_perc[7]

                
                lp.Qty_PosicionTotal = (lp.capital_base * 5) / (lp.percentsl * 2) #Cual es el total de la posicion en base al capital base para que el SL este en 2,5% de perdida.
                lp.PF_esperado[1] = (lp.recorrido_perc[1] / lp.sum_recorrrido_perc) * (lp.Qty_PosicionTotal * (lp.percentsl/100)) #Calculo del profit esperado de cada SubPosicion
                lp.PF_esperado[2] = (lp.recorrido_perc[2] / lp.sum_recorrrido_perc) * (lp.Qty_PosicionTotal * (lp.percentsl/100))
                lp.PF_esperado[3] = (lp.recorrido_perc[3] / lp.sum_recorrrido_perc) * (lp.Qty_PosicionTotal * (lp.percentsl/100))
                lp.PF_esperado[4] = (lp.recorrido_perc[4] / lp.sum_recorrrido_perc) * (lp.Qty_PosicionTotal * (lp.percentsl/100))
                lp.PF_esperado[5] = (lp.recorrido_perc[5] / lp.sum_recorrrido_perc) * (lp.Qty_PosicionTotal * (lp.percentsl/100))
                if lp.input_niveles > 5:
                    lp.PF_esperado[6] = (lp.recorrido_perc[6] / lp.sum_recorrrido_perc) * (lp.Qty_PosicionTotal * (lp.percentsl/100))
                    lp.PF_esperado[7] = (lp.recorrido_perc[7] / lp.sum_recorrrido_perc) * (lp.Qty_PosicionTotal * (lp.percentsl/100))
                lp.sum_PF_esperado = lp.PF_esperado[1] + lp.PF_esperado[2] + lp.PF_esperado[3] + lp.PF_esperado[4] + lp.PF_esperado[5] +lp.PF_esperado[6] + lp.PF_esperado[7]

                lp.Qty_USDT_SubPosicion = lp.PF_esperado[1] / lp.recorrido_perc[1] #Cantidad de USDT de cada sub posicion
                if lp.input_niveles > 5:lp.sum_Qty_USDT_SubPosicion = lp.Qty_USDT_SubPosicion * 7
                else:lp.sum_Qty_USDT_SubPosicion = lp.Qty_USDT_SubPosicion * 5

                lp.Qty_mVar[1] = lp.Qty_USDT_SubPosicion / lp.Po_valor[1] #Cantidad de moneda de cada sub posicion
                lp.Qty_mVar[2] = lp.Qty_USDT_SubPosicion / lp.Po_valor[2]
                lp.Qty_mVar[3] = lp.Qty_USDT_SubPosicion / lp.Po_valor[3]
                lp.Qty_mVar[4] = lp.Qty_USDT_SubPosicion / lp.Po_valor[4]
                lp.Qty_mVar[5] = lp.Qty_USDT_SubPosicion / lp.Po_valor[5]
                if lp.input_niveles > 5:
                    lp.Qty_mVar[6] = lp.Qty_USDT_SubPosicion / lp.Po_valor[6]
                    lp.Qty_mVar[7] = lp.Qty_USDT_SubPosicion / lp.Po_valor[7]
                lp.sum_Qty_mVar = lp.Qty_mVar[1] + lp.Qty_mVar[2] + lp.Qty_mVar[3] + lp.Qty_mVar[4] + lp.Qty_mVar[5] + lp.Qty_mVar[6] + lp.Qty_mVar[7]

                lp.perc_SubSL1 = (lp.Po_valor[1] - lp.precio_banda) / lp.Po_valor[1] #Distancia porcentual de PE y el SL de cada Sub Posicion
                lp.valor_SubSL1 = lp.perc_SubSL1 * lp.Qty_USDT_SubPosicion #Valor de perdida que me dara el SL de cada Sub Posicion

                 
                #### Estos calculos de toques son en base al escalon 1 que es el de menos perdida,
                #### tendria que hacerlo en el escalon del medio para ser mas fidedigno.
                lp.T4_valorperdida = sum((lp.valor_SubSL1*2) * (2 ** i) for i in range(4))#valor de la perdida en cada toque
                lp.T5_valorperdida = sum((lp.valor_SubSL1*2) * (2 ** i) for i in range(5))
                lp.T6_valorperdida = sum((lp.valor_SubSL1*2) * (2 ** i) for i in range(6))
                lp.T4_percperdida = lp.T4_valorperdida / lp.capital_base #porcentaje del capital total que representa la perdida en cada toque
                lp.T5_percperdida = lp.T5_valorperdida / lp.capital_base
                lp.T6_percperdida = lp.T6_valorperdida / lp.capital_base
                lp.T4_MaxUSDTQty = lp.T4_valorperdida / lp.perc_SubSL1 #Volumen de la posicion a abrir en ese toque
                lp.T5_MaxUSDTQty = lp.T5_valorperdida / lp.perc_SubSL1
                lp.T6_MaxUSDTQty = lp.T6_valorperdida / lp.perc_SubSL1



                #################################################  LOGICA DE POSICIONES #################################################################

                #######################################################################################################################################
                ####################################################### INICIO PO1 #######################################################################
                #######################################################################################################################################
                
                ############################################################### POS1 ####################################################################
                if lp.current_price <= lp.Po_valor[1] and not rt.control_pos[1]: 
                    rt.control_pos[1] = True
                    rt.PE_Pos[1] = lp.current_price 
                    splittage = (lp.Po_valor[1] - rt.PE_Pos[1]) 
                    rt.SL_Pos[1] = lp.precio_banda - splittage #Establece el TP y el SL en base al precio tomado, mueve el sl y el tp de igual manera que el PE
                    rt.TP_Pos[1] = lp.step_valor[1] - splittage

                    rt.Qty_USDT_SubPosicion = lp.PF_esperado[1] / ((rt.PE_Pos[1]  - lp.limite_inferior) / rt.PE_Pos[1] ) #el segundo termino de la division es el recorrido_perc[1] pero calculado en el PE
                    rt.Qty_mVar[1] = rt.Qty_USDT_SubPosicion / rt.PE_Pos[1] 
                    rt.Qty_mVar_rec_acum[1] = (abs(sum(rt.PnL_SL1_array)) / (1 - (rt.TP_Pos[1] / rt.PE_Pos[1])))/rt.PE_Pos[1] #Calcula la cobertura necesaria en base al balance negativo.
                                                     
                    #Condiciones para eliminar pequenios saldos del balance general de posicion 1.
                    if rt.Qty_mVar_rec_acum[1] == 0 and rt.Bal_Pos[1] < 0: #rt.Qty_mVar_rec_acum[1] == 0 se refiere a que  rt.PnL_SL1_array, es decir viene de un SL luego de un TP, y que rt.Bal_Pos[1] es negativo
                        equidad_balance = (abs(rt.Bal_Pos[1]) / (1 - (rt.TP_Pos[1] / rt.PE_Pos[1])))/rt.PE_Pos[1] 
                    elif rt.Qty_mVar_rec_acum[1] == 0 and rt.Bal_Pos[1] > 0:#aca hace que reste a rec_acum ya que el saldo es positivo
                        equidad_balance = -abs(rt.Bal_Pos[1] / (1 - (rt.TP_Pos[1] / rt.PE_Pos[1]))/rt.PE_Pos[1])
                    else:
                        equidad_balance = 0

                    rt.Qty_mVar_rec[1] =  rt.Qty_mVar[1] + rt.Qty_mVar_rec_acum[1] + equidad_balance
                    Qty_To_Open1 = rt.Qty_mVar[1] + rt.Qty_mVar_rec[1]  #Cantidad a pasar a la solicitud
                 
                    wcsv.id_posicion = wcsv.id_posicion + 1
                    wcsv.type_Pos = "Po1"
                    Data_csv = [
                        [
                        wcsv.id_posicion,
                        wcsv.type_Pos,
                        f"{rt.SL_Pos[1]:.2f}",
                        f"{rt.PE_Pos[1]:.2f}",   
                        f"{rt.TP_Pos[1]:.2f}",
                        f"{rt.Qty_USDT_SubPosicion:.2f}",
                        f"{rt.Qty_mVar[1]:.3f}",
                        f"{rt.Qty_mVar_rec[1]:.3f}",
                        f"{Qty_To_Open1:.3f}",
                        f"{rt.cont_hits[1]}",
                        f"{rt.Bal_Pos[1]:.2f}"
                                            
                        ]
                    ]
                    write_csv(Data_csv)
                    
                ############################################################### TP1 ###################################################################
                if lp.current_price <= rt.TP_Pos[1] and not rt.control_TP[1]: 
                    rt.control_TP[1] = True
                    wcsv.type_Pos = "TP1"
                    rt.PE_TP_Pos[1] = lp.current_price
                    Qty_TakeTP = rt.Qty_mVar_rec[1] #cerrar y tomar ganancias del recupero
                    rt.Pnl_TP[1] =  (rt.Qty_mVar_rec[1] * rt.PE_Pos[1]) - (rt.Qty_mVar_rec[1] * rt.PE_TP_Pos[1])
                    
                    rt.cont_hits[1] = 0 #Vuevle a cero el contador de toques

                    rt.Bal_Pos[1] = rt.Bal_Pos[1] + rt.Pnl_TP[1]

                    wcsv.id_posicion = wcsv.id_posicion + 1
                    Data_csv = [
                        [
                        wcsv.id_posicion,
                        wcsv.type_Pos,
                        f"{rt.PE_TP_Pos[1]:.2f}",
                        f"{Qty_TakeTP:.3f}",
                        f"{rt.Pnl_TP[1]:.2f}",
                        f"{rt.Bal_Pos[1]:.2f}"

                        ]
                    ]
                    write_csv(Data_csv)

                    rt.Qty_mVar_rec[1] = 0
                    rt.Qty_mVar_rec_acum[1] = 0
                    rt.PnL_SL1_array.clear()

                ############################################################### SL1 ###################################################################
                if lp.current_price >= rt.SL_Pos[1] and rt.control_pos[1]: 
                    rt.control_pos[1] = False
                    rt.PE_SL_Pos[1] = lp.current_price 
                    Qty_To_Close1 = rt.Qty_mVar[1] + rt.Qty_mVar_rec[1] #Si paso por el TP la Qty_mVar1_rec va a ser cero y va a cerrar solo la parte pura, en el SL debe quedar todo cerrado.
                    
                    rt.PnL_SL[1] =  (Qty_To_Close1 * rt.PE_Pos[1]) - (Qty_To_Close1 * rt.PE_SL_Pos[1]) #Calcula la perdida de la posicion abierta que se esta cerrando
                    rt.PnL_SL1_array.append(rt.PnL_SL[1]) #Agrega la perdida al array
                    sum_PnlArray = sum(rt.PnL_SL1_array) #Sumatoria de perdidas acumuladas

                    rt.Bal_Pos[1] =  rt.Bal_Pos[1] + rt.PnL_SL[1]

                    if not rt.control_TP[1]: #si no toco TP1
                       rt.cont_hits[1] = rt.cont_hits[1] + 1

                    wcsv.id_posicion = wcsv.id_posicion + 1
                    wcsv.type_Pos = "SL1"
                    Data_csv = [
                        [
                        wcsv.id_posicion,
                        wcsv.type_Pos,
                        f"{rt.PE_SL_Pos[1]:.2f}",
                        f"{sum_PnlArray:.2f}",
                        f"{rt.PnL_SL[1]:.2f}",  
                        f"{rt.Qty_mVar[1]:.3f}",
                        f"{rt.Qty_mVar_rec[1]:.3f}",
                        f"{Qty_To_Close1:.3f}",
                        f"{rt.cont_hits[1]}",
                        f"{rt.Bal_Pos[1]:.2f}" 
                        ]
                    ]
                    write_csv(Data_csv)
                    if rt.control_TP[1]: rt.PnL_SL1_array.pop() #Elimina el ultimo PnL agregado que es el de cerrar la posicion pura, para que no abra ese monto como recupero ya que toco el TP
                    
                    rt.control_TP[1] = False
                    rt.SL_Pos[1] = 0
                    rt.PE_Pos[1] = 0
                    rt.TP_Pos[1] = 0
                    rt.Qty_USDT_SubPosicion = 0
                    rt.ValorPuro_Pos[1] = 0
                    rt.Qty_mVar[1] = 0

                #######################################################################################################################################
                ####################################################### FIN PO1 #######################################################################
                #######################################################################################################################################

                
                
                if rt.control_pos[1]:
                    rt.ValorPuro_Pos[1] = rt.Qty_USDT_SubPosicion * ((rt.PE_Pos[1]  - lp.current_price ) / rt.PE_Pos[1] ) 
                
            
        time.sleep(1)    


#Puesta en funcionamiento del sokcket de binance llamando a la funcion principal.
async def start_socket(precio_banda_post, niveles_post_form, sl_post_form, sloption_post_form, current_price_form):
    bsm = BinanceSocketManager(client)
    socket = bsm.symbol_ticker_socket(symbol)

    ## PASO LOS VALORES POST A LAS VARIABLES DE LA CLASE
    lp.precio_banda = float(precio_banda_post)
    lp.input_niveles = int(niveles_post_form)
    lp.input_sloption  = int(sloption_post_form)
    lp.input_sl = float(sl_post_form)
    lp.capital_base = 10000 
    #lp.current_price = float(current_price_form) #esto es para simular un precio en concreto. (lo puedo borrar)

    async with socket as s:
        while True:
            msg = await s.recv()  
            calculos(msg)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_socket())


def write_csv(Data_csv): #Funcion que escribe el csv
    with open("static/registro_posiciones.csv", mode='a', newline='', encoding='utf-8') as archivo: 
        escritor_csv = csv.writer(archivo)
        escritor_csv.writerows(Data_csv)


def crear_csv(): #Funcion que crea el csv
    with open("static/registro_posiciones.csv", mode='w', newline='', encoding='utf-8') as archivo:
        pass  
    print("Archivo CSV creado o vaciado exitosamente.")
crear_csv()  




