import xmlrpc.client

proxy = xmlrpc.client.ServerProxy("http://localhost:9001/")

while True:
    print("\n1. Đăng ký dịch vụ")
    print("2. Tra cứu dịch vụ")
    print("3. Xóa dịch vụ")
    print("0. Thoát")
    choice = input("Chọn thao tác: ")
    
    if choice == "1":
        name = input("Tên dịch vụ: ")
        addr = input("Địa chỉ IP:Port: ")
        print(proxy.register(name, addr))
    elif choice == "2":
        name = input("Tên dịch vụ cần tra: ")
        print("→", proxy.lookup(name))
    elif choice == "3":
        name = input("Tên dịch vụ cần xóa: ")
        print(proxy.unregister(name))
    elif choice == "0":
        break