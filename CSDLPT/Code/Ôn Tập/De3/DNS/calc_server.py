from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client

def add(a, b):
    print(f"Tính {a} + {b}")
    return a + b

# Đăng ký với naming service
naming = xmlrpc.client.ServerProxy("http://localhost:8000")
print(naming)
naming.register("calc_service", "http://localhost:9000")

# Bắt đầu RPC server
server = SimpleXMLRPCServer(("localhost", 9000))
server.register_function(add, "add")
print("Calc Service đang chạy tại cổng 9000...")
server.serve_forever()
