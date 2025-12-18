import socket
import threading

server_address = ("127.0.0.1", 5001)

# Tạo socket UDP
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind client với một cổng bất kỳ để nhận tin nhắn từ server
client.bind(("0.0.0.0", 0))  

def receive_messages():
    """Luồng nhận tin nhắn từ server"""
    while True:
        try:
            message, _ = client.recvfrom(1024)
            print("\nTin nhắn từ server:", message.decode())
        except OSError as e:
            print("Lỗi khi nhận tin nhắn:", e)
            break  # Dừng luồng nếu có lỗi

# Tạo và chạy luồng nhận tin nhắn
thread = threading.Thread(target=receive_messages, daemon=True)
thread.start()

print("Nhập tin nhắn để gửi (gõ 'exit' để thoát):")

while True:
    message = input()
    if message.lower() == "exit":
        print("Đang thoát...")
        break
    client.sendto(message.encode(), server_address)

# Đóng socket sau khi thoát
client.close()
