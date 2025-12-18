import socket

def start_client():
    # Tạo socket UDP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Địa chỉ server
    server_address = ('localhost', 12345)
    
    print("Client UDP đã khởi động. Nhập 'exit' hoặc 'tạm biệt' để kết thúc.")
    print("Bạn có thể hỏi server về: thời tiết, giờ hiện tại, tin tức, giá bitcoin")
    
    while True:
        # Nhập tin nhắn từ bàn phím
        message = input("Nhập tin nhắn gửi đến server: ")
        
        # Gửi tin nhắn đến server
        client_socket.sendto(message.encode('utf-8'), server_address)
        
        # Kiểm tra nếu người dùng muốn thoát
        if message.lower() in ['exit', 'quit', 'tạm biệt']:
            print("Đang đóng kết nối...")
            break
        
        # Nhận phản hồi từ server
        data, _ = client_socket.recvfrom(1024)
        print(f"Phản hồi từ server: {data.decode('utf-8')}\n")
    
    client_socket.close()
    print("Client đã đóng kết nối.")

if __name__ == "__main__":
    start_client()