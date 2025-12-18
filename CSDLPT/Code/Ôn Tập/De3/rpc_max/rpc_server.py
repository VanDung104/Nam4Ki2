from flask import Flask, request, jsonify
import requests, threading, time, sys
from utils import get_primes

NAME_SERVER = 'http://localhost:5000'
SERVICE_NAME = 'prime_service'

port = int(sys.argv[1]) if len(sys.argv) > 1 else 6000
ADDRESS = f'http://localhost:{port}'

app = Flask(__name__)

@app.route('/primes', methods=['POST'])
def primes():
    data = request.json['numbers']
    result = get_primes(data)
    return jsonify(result)

def heartbeat():
    while True:
        try:
            requests.post(f'{NAME_SERVER}/heartbeat', json={'service_name': SERVICE_NAME, 'address': ADDRESS})
        except: pass
        time.sleep(5)

if __name__ == '__main__':
    requests.post(f'{NAME_SERVER}/register', json={'service_name': SERVICE_NAME, 'address': ADDRESS})
    threading.Thread(target=heartbeat, daemon=True).start()
    app.run(port=port)