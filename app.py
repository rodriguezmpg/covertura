from flask import Flask, render_template, jsonify, request
import threading
import trading_loop
import recording


app=Flask(__name__)



@app.route('/')
def index():
    return render_template('index.html')





@app.route('/datos')
def datos():
    return jsonify({
        'precio_banda': trading_loop.loop_class.precio_banda,
        'Cprecio': trading_loop.loop_class.current_price

    })

@app.route('/main')
def index_backtest():
    return render_template('main_loop.html')

@app.route('/mainstart', methods=['POST'])
def start_trading():
    precio_banda_post = request.form.get('precio_banda_post_form')
    niveles_post_form = request.form.get('niveles_post_form')
    percentsl_post_form = request.form.get('percentsl_post_form')

    main_thread = threading.Thread(
        target=trading_loop.main_loop,
        args=(precio_banda_post, niveles_post_form, percentsl_post_form)
    )
    main_thread.start()
    return render_template('main_loop.html')




@app.route('/recordstart')
def start_record():
    recording_thread = threading.Thread(target=recording.recording_loop)
    recording_thread.start()
    return "Grabando"


app.run(debug=True, use_reloader=False) # Esta linea es lo que pone a funcionar el flask







   # try:
        #     orden = client.futures_create_order(
        #         symbol='ETHUSDT',           
        #         side=SIDE_SELL,              
        #         type=ORDER_TYPE_MARKET,     
        #         quantity=0.01              
        #     )
        #     print(f"Orden abierta exitosamente: {orden}")

        # except Exception as e:
        #     print(f"Ocurrió un error: {e}")

        # try:
        #     orden = client.futures_create_order(
        #         symbol='ETHUSDT',           
        #         side=SIDE_BUY,              
        #         type=ORDER_TYPE_MARKET,     
        #         quantity=0.01              
        #     )
        #     print(f"Orden cerrada exitosamente: {orden}")

        # except Exception as e:
        #     print(f"Ocurrió un error: {e}")