import zmq

def server():
    context = zmq.Context()
    socket = context.socket(zmq.REP)  # Tạo socket trả lời (reply)
    socket.bind("tcp://*:12345")  # Lắng nghe trên cổng 12345

    print("Server đang chạy...")

    while True:
        message = socket.recv()  # Chờ nhận tin nhắn
        message_str = message.decode()  # Giải mã tin nhắn

        if message_str == "STOP":  # Nếu nhận được "STOP", dừng server
            socket.send(b"Server stopping...")  # Gửi phản hồi cuối cùng
            break

        reply = message_str + "*"  # Thêm ký tự "*" vào tin nhắn
        socket.send(reply.encode())  # Gửi phản hồi

    socket.close()  # Đóng socket
    context.term()  # Giải phóng tài nguyên
    print("Server đã dừng.")

def client():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)  # Tạo socket yêu cầu (request)

    socket.connect("tcp://localhost:12345")  # Kết nối tới server

    socket.send(b"Hello world")  # Gửi tin nhắn
    message = socket.recv()  # Nhận phản hồi từ server
    print(f"Phản hồi từ server: {message.decode()}")

    socket.send(b"STOP")  # Yêu cầu server dừng
    message = socket.recv()  # Nhận phản hồi cuối cùng từ server
    print(f"Server trả lời: {message.decode()}")

    socket.close()  # Đóng socket
    context.term()  # Giải phóng tài nguyên

# Chạy server trước, sau đó chạy client để kiểm tra
if __name__ == "__main__":
    from multiprocessing import Process

    # Chạy server trong một tiến trình riêng
    server_process = Process(target=server)
    server_process.start()

    # Chạy client
    client()

    # Chờ server kết thúc
    server_process.join()
