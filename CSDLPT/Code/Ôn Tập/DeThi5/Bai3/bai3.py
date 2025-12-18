from flask import Flask, request, jsonify

app = Flask(__name__)

name_server = {}

@app.route('/register', methods=['POST'])
def register_name():
    data = request.get_json()
    if 'name' not in data or 'address' not in data or 'service' not in data:
        return jsonify({"error": "Missing 'name', 'address', or 'service' in the request"}), 400

    name = data['name']
    address = data['address']
    service = data['service']

    name_server[name] = {'address': address, 'service': service}

    return jsonify({"message": f"Successfully registered {name} -> {address} for service {service}"}), 200

@app.route('/resolve/<name>', methods=['GET'])
def resolve_name(name):
    if name in name_server:
        data = name_server[name]
        return jsonify({
            "name": name,
            "address": data['address'],
            "service": data['service']
        }), 200
    else:
        return jsonify({"error": "Name not found"}), 404

@app.route('/unregister/<name>', methods=['DELETE'])
def unregister_name(name):
    if name in name_server:
        del name_server[name]
        return jsonify({"message": f"Successfully unregistered {name}"}), 200
    else:
        return jsonify({"error": "Name not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
