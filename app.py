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
        'precio_banda': trading_loop.loop_class.precio_banda,
        'Cprecio': trading_loop.loop_class.current_price,
        'contador': trading_loop.loop_class.contador
    })

@app.route('/main')
def index_backtest():
    return render_template('main_loop.html')

@app.route('/mainstart', methods=['POST'])
def start_trading():
    precio_banda_post = request.form.get('precio_banda_post_form')
    niveles_post_form = request.form.get('niveles_post_form')
    percentsl_post_form = request.form.get('percentsl_post_form')
    asyncio.run(trading_loop.start_socket(precio_banda_post, niveles_post_form, percentsl_post_form))
    return render_template('main_loop.html')




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True, use_reloader=False)

