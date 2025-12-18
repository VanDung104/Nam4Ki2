import socket
import pickle
import struct

def sum_partial(numbers):
    """Hàm tính tổng một phần danh sách."""
    return sum(numbers)

def receive_full_data(conn):
    """Nhận dữ liệu từ socket theo độ dài được gửi trước"""
    raw_msglen = conn.recv(4)  # Đọc 4 byte đầu để biết kích thước dữ liệu
    if not raw_msglen:
        return None
    msglen = struct.unpack(">I", raw_msglen)[0]  # Giải mã thành số nguyên

    data = b""
    while len(data) < msglen:
        packet = conn.recv(4096)  # Nhận từng gói
        if not packet:
            break
        data += packet
    return data

def worker_server(port):
    """Worker xử lý dữ liệu từ Server"""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", port))
    server.listen(5)
    print(f"Worker đang chạy trên cổng {port}...")

    while True:
        conn, addr = server.accept()
        data = receive_full_data(conn)  # Đọc toàn bộ dữ liệu từ Server
        
        if data:
            numbers = pickle.loads(data)  # Giải mã dữ liệu
            print(f"Nhận {len(numbers)} số từ {addr}, xử lý...")

            result = sum_partial(numbers)
            result_data = pickle.dumps(result)
            conn.sendall(struct.pack(">I", len(result_data)))  # Gửi kích thước kết quả
            conn.sendall(result_data)  # Gửi dữ liệu kết quả
        else:
            print(f"Lỗi: Không nhận được dữ liệu từ {addr}")

        conn.close()

if __name__ == "__main__":
    port = int(input("Nhập cổng Worker (ví dụ: 5001, 5002): "))
    worker_server(port)
