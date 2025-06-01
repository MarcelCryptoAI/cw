from flask import Flask, jsonify
from flask_cors import CORS
from pybit.unified_trading import HTTP
from dotenv import load_dotenv
import os

app = Flask(__name__)
CORS(app)
load_dotenv(dotenv_path='backend/.env')

BYBIT_API_KEY = os.getenv("BYBIT_API_KEY")
BYBIT_API_SECRET = os.getenv("BYBIT_API_SECRET")
BYBIT_ACCOUNT_TYPE = os.getenv("BYBIT_ACCOUNT_TYPE", "UNIFIED")

session = HTTP(
    testnet=False,
    api_key=BYBIT_API_KEY,
    api_secret=BYBIT_API_SECRET
)

@app.route('/api/open-positions', methods=['GET'])
def open_positions():
    positions = session.get_positions(category="linear")  # pas category aan voor futures/spot
    data = positions.get('result', {}).get('list', [])
    return jsonify(data)

@app.route('/api/open-orders', methods=['GET'])
def open_orders():
    orders = session.get_open_orders(category="linear")  # pas category aan voor futures/spot
    data = orders.get('result', {}).get('list', [])
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
