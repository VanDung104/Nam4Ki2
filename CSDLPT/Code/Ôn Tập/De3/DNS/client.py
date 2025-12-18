import xmlrpc.client

# Tra cứu địa chỉ từ naming service
naming = xmlrpc.client.ServerProxy("http://localhost:8000")
address = naming.resolve("calc_service")

if not address:
    print("Không tìm thấy dịch vụ 'calc_service'")
else:
    service = xmlrpc.client.ServerProxy(address)
    a = int(input("Nhập số thứ nhất: "))
    b = int(input("Nhập số thứ hai: "))
    result = service.add(a, b)
    print(f"Kết quả: {a} + {b} = {result}")
