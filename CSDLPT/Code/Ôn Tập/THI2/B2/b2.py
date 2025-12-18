from multiprocessing import Process, Queue
import time
import random

# Kiểu tin nhắn
ACQUIRE = "acquire"
RELEASE = "release"
GRANT = "grant"

def lock_server(request_queue, response_queues):
    lock_holder = None
    waiting_queue = []

    while True:
        if not request_queue.empty():
            client_id, msg_type = request_queue.get()
            
            if msg_type == ACQUIRE:
                print(f"[MÁY CHỦ] Nhận yêu cầu GIỮ KHÓA từ Tiến trình-{client_id}")
                if lock_holder is None:
                    lock_holder = client_id
                    response_queues[client_id].put(GRANT)
                    print(f"[MÁY CHỦ] ĐÃ CẤP KHÓA cho Tiến trình-{client_id}")
                else:
                    waiting_queue.append(client_id)
                    print(f"[MÁY CHỦ] Tiến trình-{client_id} đã được thêm vào hàng đợi")

            elif msg_type == RELEASE:
                print(f"[MÁY CHỦ] Nhận yêu cầu THẢ KHÓA từ Tiến trình-{client_id}")
                if lock_holder == client_id:
                    lock_holder = None
                    if waiting_queue:
                        next_client = waiting_queue.pop(0)
                        lock_holder = next_client
                        response_queues[next_client].put(GRANT)
                        print(f"[MÁY CHỦ] ĐÃ CẤP KHÓA cho Tiến trình-{next_client}")
                else:
                    print(f"[MÁY CHỦ] CẢNH BÁO: Tiến trình-{client_id} cố gắng thả khóa nhưng không sở hữu!")

def client_process(client_id, request_queue, response_queue):
    while True:
        # Gửi yêu cầu giữ khóa
        print(f"[Tiến trình-{client_id}] Gửi yêu cầu giữ khóa...")
        request_queue.put((client_id, ACQUIRE))

        # Đợi máy chủ phản hồi
        msg = response_queue.get()
        if msg == GRANT:
            print(f"[Tiến trình-{client_id}] ĐÃ GIỮ KHÓA! Đang xử lý công việc...")
            time.sleep(random.uniform(1, 3))
            print(f"[Tiến trình-{client_id}] Đang thả khóa...")
            request_queue.put((client_id, RELEASE))
            time.sleep(random.uniform(1, 3))

if __name__ == "__main__":
    request_queue = Queue()
    response_queues = {i: Queue() for i in range(3)}

    # Tạo tiến trình máy chủ
    server = Process(target=lock_server, args=(request_queue, response_queues))
    server.start()

    # Tạo 3 tiến trình client
    clients = []
    for i in range(3):
        p = Process(target=client_process, args=(i, request_queue, response_queues[i]))
        clients.append(p)
        p.start()

    # Mô phỏng chạy trong 30 giây rồi dừng lại
    time.sleep(30)
    for p in clients:
        p.terminate()
    server.terminate()
