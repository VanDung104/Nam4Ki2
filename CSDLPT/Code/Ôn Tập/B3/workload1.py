import socket
import pickle
import struct
import math

def is_prime(n):
    """Kiểm tra số nguyên tố"""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    w = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += w
        w = 6 - w
    return True

def check_primes(numbers):
    """Kiểm tra và trả về danh sách số nguyên tố"""
    return [n for n in numbers if is_prime(n)]

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
    """Worker xử lý kiểm tra số nguyên tố"""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", port))
    server.listen(5)
    print(f"Worker kiểm tra số nguyên tố đang chạy trên cổng {port}...")

    while True:
        conn, addr = server.accept()
        data = receive_full_data(conn)  # Đọc toàn bộ dữ liệu từ Server
        
        if data:
            numbers = pickle.loads(data)  # Giải mã dữ liệu
            print(f"Nhận {len(numbers)} số từ {addr}, đang kiểm tra...")

            primes = check_primes(numbers)  # Kiểm tra số nguyên tố
            result_data = pickle.dumps(primes)
            conn.sendall(struct.pack(">I", len(result_data)))  # Gửi kích thước
            conn.sendall(result_data)  # Gửi kết quả
        else:
            print(f"Lỗi: Không nhận được dữ liệu từ {addr}")

        conn.close()

if __name__ == "__main__":
    port = int(input("Nhập cổng Worker (ví dụ: 5001, 5002): "))
    worker_server(port)