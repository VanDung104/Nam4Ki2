from xmlrpc.server import SimpleXMLRPCServer
import json
import os

DB_FILE = 'D://Nam4Ki2//CSDLPT//Code//Ôn Tập//De3//DNS//service_registry.json'

def load_registry():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_registry(data):
    with open(DB_FILE, 'w') as f:
        json.dump(data, f)

registry = load_registry()

def register(name, address):
    registry[name] = address
    save_registry(registry)
    print(f"Đã đăng ký: {name} -> {address}")
    return True

def resolve(name):
    return registry.get(name, "")

server = SimpleXMLRPCServer(("localhost", 8000))
server.register_function(register, "register")
server.register_function(resolve, "resolve")
print("Naming Service đang chạy tại cổng 8000...")
server.serve_forever()
