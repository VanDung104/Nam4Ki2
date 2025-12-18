import socket

HOST = '127.0.0.1'  # Địa chỉ IP của server
PORT = 12345        # Cổng của server

class Client:
    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Tạo socket TCP
        s.connect((HOST, PORT))  # Kết nối tới server

        s.send(b"Hello, world")  # Gửi thông điệp tới server
        data = s.recv(1024)  # Nhận phản hồi từ server
        print(f"Phản hồi từ server: {data.decode()}")  # In phản hồi

        s.close()  # Đóng kết nối

# Chạy client
if __name__ == "__main__":
    client = Client()
    client.run()
