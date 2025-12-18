from xmlrpc.server import SimpleXMLRPCServer

service_registry = {}

def register(service_name, address):
    service_registry[service_name] = address
    return f"Đã đăng ký {service_name} → {address}"

def lookup(service_name):
    return service_registry.get(service_name, "Không tìm thấy dịch vụ.")

def unregister(service_name):
    if service_name in service_registry:
        del service_registry[service_name]
        return f"Đã xóa dịch vụ {service_name}"
    return "Không tìm thấy dịch vụ để xóa."

server = SimpleXMLRPCServer(("localhost", 9001))
server.register_function(register, "register")
server.register_function(lookup, "lookup")
server.register_function(unregister, "unregister")
print("Name Server chạy tại cổng 9001...")
server.serve_forever()