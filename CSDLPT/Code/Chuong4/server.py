from socket import *

HOST = '127.0.0.1'  # Địa chỉ IP của server (localhost)
PORT = 12345        # Cổng lắng nghe

class Server:
    def run(self):
        s = socket(AF_INET, SOCK_STREAM)  # Tạo socket TCP
        s.bind((HOST, PORT))              # Gán địa chỉ và cổng cho socket
        s.listen(1)                        # Lắng nghe kết nối từ client

        print(f"Server đang chạy trên {HOST}:{PORT}...")
        conn, addr = s.accept()  # Chấp nhận kết nối từ client
        print(f"Kết nối từ: {addr}")

        while True:
            data = conn.recv(1024)  # Nhận dữ liệu từ client
            if not data:
                break  # Thoát vòng lặp nếu không có dữ liệu

            conn.send(data + b"*")  # Gửi lại dữ liệu kèm ký tự "*"

        conn.close()  # Đóng kết nối
        print("Kết nối đã đóng.")

# Chạy server
if __name__ == "__main__":
    server = Server()
    server.run()
