import socket

def start_server():
    # Tạo socket UDP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Bind địa chỉ và port
    server_address = ('localhost', 12345)
    server_socket.bind(server_address)
    print("Server đang chạy và lắng nghe trên port 12345...")
    
    # Dữ liệu mô phỏng cho các câu hỏi
    responses = {
        "thời tiết hôm nay": "Hôm nay trời nắng, nhiệt độ 28-32°C",
        "giờ hiện tại": "Bây giờ là 10:30 AM",
        "tin tức mới nhất": "Tin mới: Python 4.0 sẽ ra mắt vào năm 2025",
        "giá bitcoin": "Giá Bitcoin hiện tại: $50,000",
        "chào server": "Xin chào! Tôi là server UDP. Bạn có thể hỏi tôi về: thời tiết, giờ hiện tại, tin tức, hoặc giá bitcoin",
        "tạm biệt": "Tạm biệt! Hẹn gặp lại bạn lần sau!"
    }
    
    print("Server sẵn sàng nhận tin nhắn...")
    
    while True:
        # Nhận dữ liệu từ client
        data, client_address = server_socket.recvfrom(1024)
        question = data.decode('utf-8').lower()
        print(f"Nhận từ client [{client_address}]: {question}")
        
        # Kiểm tra nếu client gửi "exit" hoặc "tạm biệt"
        if question in ["exit", "quit", "tạm biệt"]:
            response = responses.get("tạm biệt", "Tạm biệt!")
            server_socket.sendto(response.encode('utf-8'), client_address)
            print(f"Client {client_address} đã ngắt kết nối")
            continue
        
        # Tìm câu trả lời phù hợp
        response = responses.get(question, "Xin lỗi, tôi không hiểu câu hỏi của bạn. Bạn có thể hỏi về: thời tiết, giờ hiện tại, tin tức, hoặc giá bitcoin")
        
        # Gửi câu trả lời
        server_socket.sendto(response.encode('utf-8'), client_address)
        print(f"Đã gửi phản hồi: {response}")

if __name__ == "__main__":
    start_server()