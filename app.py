from flask import Flask
from binance.client import Client
from binance.enums import *

app = Flask(__name__)


print "Hello"

# @app.route('/')
# def hello_world():
#     return 'Hello, World!'





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
