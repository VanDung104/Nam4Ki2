from flask import Flask, request, jsonify
import threading, time

app = Flask(__name__)
registry = {}
HEARTBEAT_TIMEOUT = 10

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    name = data['service_name']
    addr = data['address']
    registry.setdefault(name, {})[addr] = time.time()
    return 'Registered', 200

@app.route('/heartbeat', methods=['POST'])
def heartbeat():
    data = request.json
    name = data['service_name']
    addr = data['address']
    if name in registry and addr in registry[name]:
        registry[name][addr] = time.time()
    return 'OK', 200

@app.route('/resolve/<service_name>', methods=['GET'])
def resolve(service_name):
    now = time.time()
    if service_name in registry:
        alive = [addr for addr, t in registry[service_name].items() if now - t <= HEARTBEAT_TIMEOUT]
        return jsonify(alive)
    return jsonify([])

def cleanup():
    while True:
        time.sleep(5)
        now = time.time()
        for name in list(registry):
            for addr in list(registry[name]):
                if now - registry[name][addr] > HEARTBEAT_TIMEOUT:
                    del registry[name][addr]

if __name__ == '__main__':
    threading.Thread(target=cleanup, daemon=True).start()
    app.run(port=5000)
