from socket import *

# 1. Tạo socket
s = socket(AF_INET, SOCK_STREAM)

# 2. Bind socket với địa chỉ IP và cổng
HOST = "127.0.0.1"
PORT = 12345       # Chọn một cổng chưa sử dụng
s.bind((HOST, PORT))

# 3. Bắt đầu lắng nghe kết nối
s.listen(5)  # Cho phép tối đa 5 kết nối trong hàng chờ
print(f"Server đang lắng nghe trên {HOST}:{PORT}...")

try:
    # 4. Chấp nhận kết nối từ client
    conn, addr = s.accept()
    print(f"Kết nối từ: {addr}")
    
    while True:
        # 5. Nhận dữ liệu từ client
        data = conn.recv(1024)
        if not data:  # Nếu client ngắt kết nối, dừng vòng lặp
            break
        
        # 6. Xử lý dữ liệu
        msg = data.decode() + "*"  # Thêm ký tự "*" vào dữ liệu nhận được
        print(f"Nhận: {data.decode()} | Gửi: {msg}")
        
        # 7. Gửi phản hồi lại cho client
        conn.send(msg.encode())
finally:
    # 8. Đóng kết nối
    conn.close()
    s.close()
