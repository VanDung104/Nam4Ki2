import socket

clients = set()

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(("0.0.0.0", 5001))

print("UDP Server đang chạy trên cổng 5001...")

while True:
    message, client_addr = server.recvfrom(1024)
    
    if client_addr not in clients:
        clients.add(client_addr)

    print(f"Nhận từ {client_addr}: {message.decode()}")

    # Phát tin nhắn cho tất cả các client
    for client in clients:
        if client != client_addr:
            server.sendto(message, client)
