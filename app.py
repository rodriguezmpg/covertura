from flask import Flask, render_template, jsonify, request
import os
import trading_loop
import asyncio

app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

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
        'percentsl': round(trading_loop.lp.percentsl ,2) 
      
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

    asyncio.run(trading_loop.start_socket(precio_banda_post, niveles_post_form, sl_post_form, sloption_post_form))
    
    return render_template('main_loop.html')




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True, use_reloader=False)

