from flask import Flask, render_template, jsonify, request
import os
import trading_loop
import cp
import asyncio

app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/oporder')
def open():
    order = cp.open_order()
    ip = cp.get_public_ip()

    if ip:
        return jsonify({"order": order, "ip": ip})  # Devuelve tanto la orden como la IP en JSON
    else:
        return jsonify({"order": order, "error": "No se pudo obtener la IP"})

    return jsonify(order) 


@app.route('/datos')
def datos():
    return jsonify({
        'precio_banda': trading_loop.lp.precio_banda,
        'Cprecio': trading_loop.lp.current_price,
        'contador': trading_loop.lp.contador,
        'limite_inferior': trading_loop.lp.limite_inferior,
        'Po1_valor': round(trading_loop.lp.Po1_valor,2),
        'Po2_valor': round(trading_loop.lp.Po2_valor,2),
        'Po3_valor': round(trading_loop.lp.Po3_valor,2),
        'Po4_valor': round(trading_loop.lp.Po4_valor,2),
        'Po5_valor': round(trading_loop.lp.Po5_valor,2),
        'Po6_valor': round(trading_loop.lp.Po6_valor,2),
        'Po7_valor': round(trading_loop.lp.Po7_valor,2),
        'step1_valor': round(trading_loop.lp.step1_valor ,2),
        'step2_valor': round(trading_loop.lp.step2_valor ,2),
        'step3_valor': round(trading_loop.lp.step3_valor ,2),
        'step4_valor': round(trading_loop.lp.step4_valor ,2),
        'step5_valor': round(trading_loop.lp.step5_valor ,2),
        'step6_valor': round(trading_loop.lp.step6_valor ,2),
        'input_niveles': round(trading_loop.lp.input_niveles ,2),
        'percentsl': round(trading_loop.lp.percentsl ,2), 

        'recorrido_perc1': round(trading_loop.lp.recorrido_perc1 ,4), 
        'recorrido_perc2': round(trading_loop.lp.recorrido_perc2 ,4), 
        'recorrido_perc3': round(trading_loop.lp.recorrido_perc3 ,4), 
        'recorrido_perc4': round(trading_loop.lp.recorrido_perc4 ,4), 
        'recorrido_perc5': round(trading_loop.lp.recorrido_perc5 ,4), 
        'recorrido_perc6': round(trading_loop.lp.recorrido_perc6 ,4), 
        'recorrido_perc7': round(trading_loop.lp.recorrido_perc7 ,4),
        'sum_recorrrido_perc': round(trading_loop.lp.sum_recorrrido_perc ,4),

        'Qty_PosicionTotal': round(trading_loop.lp.Qty_PosicionTotal ,2),

        'PF_esperado1': round(trading_loop.lp.PF_esperado1 ,2), 
        'PF_esperado2': round(trading_loop.lp.PF_esperado2 ,2),
        'PF_esperado3': round(trading_loop.lp.PF_esperado3 ,2),
        'PF_esperado4': round(trading_loop.lp.PF_esperado4 ,2),
        'PF_esperado5': round(trading_loop.lp.PF_esperado5 ,2),
        'PF_esperado6': round(trading_loop.lp.PF_esperado6 ,2),
        'PF_esperado7': round(trading_loop.lp.PF_esperado7 ,2),
        'sum_PF_esperado': round(trading_loop.lp.sum_PF_esperado ,2),
        'Qty_USDT_SubPosicion': round(trading_loop.lp.Qty_USDT_SubPosicion ,2),
        'sum_Qty_USDT_SubPosicion': round(trading_loop.lp.sum_Qty_USDT_SubPosicion ,2),

        'Qty_mVar1': round(trading_loop.lp.Qty_mVar1 ,3), 
        'Qty_mVar2': round(trading_loop.lp.Qty_mVar2 ,3), 
        'Qty_mVar3': round(trading_loop.lp.Qty_mVar3 ,3), 
        'Qty_mVar4': round(trading_loop.lp.Qty_mVar4 ,3), 
        'Qty_mVar5': round(trading_loop.lp.Qty_mVar5 ,3), 
        'Qty_mVar6': round(trading_loop.lp.Qty_mVar6 ,3), 
        'Qty_mVar7': round(trading_loop.lp.Qty_mVar7 ,3), 
        'sum_Qty_mVar': round(trading_loop.lp.sum_Qty_mVar ,3), 

        'perc_SubSL': round(trading_loop.lp.perc_SubSL ,4), 
        'valor_SubSL': round(trading_loop.lp.valor_SubSL ,2),

        'T4_valorperdida': round(trading_loop.lp.T4_valorperdida,2),
        'T5_valorperdida': round(trading_loop.lp.T5_valorperdida,2),
        'T6_valorperdida': round(trading_loop.lp.T6_valorperdida,2),
        'T4_percperdida': round(trading_loop.lp.T4_percperdida,4),
        'T5_percperdida': round(trading_loop.lp.T5_percperdida,4),
        'T6_percperdida': round(trading_loop.lp.T6_percperdida,4), 
        'T4_MaxUSDTQty': round(trading_loop.lp.T4_MaxUSDTQty,2),
        'T5_MaxUSDTQty': round(trading_loop.lp.T5_MaxUSDTQty,2),
        'T6_MaxUSDTQty': round(trading_loop.lp.T6_MaxUSDTQty,2),

        'control_pos1': trading_loop.rt.control_pos1,

        'control_TP1': trading_loop.rt.control_TP1,

        'PE_Pos1': round(trading_loop.rt.PE_Pos1,2),

        'SL_Pos1': round(trading_loop.rt.SL_Pos1,2),
        
        'TP_Pos1': round(trading_loop.rt.TP_Pos1,2),

        
      
    })

@app.route('/main')
def index_backtest():
    return render_template('main_loop.html')

@app.route('/mainstart', methods=['POST'])
def start_trading():

    # REQUEST FROM FORMULARIO
    precio_banda_post = request.form.get('precio_banda_post_form')
    niveles_post_form = request.form.get('niveles_post_form')
    sl_post_form = request.form.get('sl_post_form')
    sloption_post_form = request.form.get('sloption_post_form')
    current_price_form = request.form.get('current_price_post_form') #Para simular el precio luego borrar 

    asyncio.run(trading_loop.start_socket(precio_banda_post, niveles_post_form, sl_post_form, sloption_post_form, current_price_form))
    
    return render_template('main_loop.html')




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)), debug=True, use_reloader=False)

