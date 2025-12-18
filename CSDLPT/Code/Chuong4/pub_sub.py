import multiprocessing
import zmq, time

def server():
    context = zmq.Context()
    socket = context.socket(zmq.PUB)  # Tạo socket kiểu Publisher
    socket.bind("tcp://*:12345")  # Lắng nghe trên cổng 12345

    while True:
        time.sleep(5)  # Chờ 5 giây
        t = "TIME " + time.asctime()  # Lấy thời gian hiện tại
        socket.send(t.encode())  # Gửi thời gian đi (publish)
def client():
    context = zmq.Context()
    socket = context.socket(zmq.SUB)  # Tạo socket kiểu Subscriber
    socket.connect("tcp://localhost:12345")  # Kết nối đến server
    socket.setsockopt(zmq.SUBSCRIBE, b"TIME")  # Chỉ nhận tin nhắn có prefix "TIME"

    for i in range(5):  # Nhận 5 tin nhắn
        time_msg = socket.recv()  # Nhận tin nhắn
        print(time_msg.decode())  # In tin nhắn ra màn hình
if __name__ == "__main__":
    from multiprocessing import Process

    # Chạy server trong một tiến trình riêng
    server_process = Process(target=server)
    server_process.start()

    # Chạy client
    client()

    # Chờ client kết thúc
    server_process.terminate()  # Dừng server
    server_process.join()
