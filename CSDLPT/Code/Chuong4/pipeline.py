from multiprocessing import Process
import random, pickle, time, zmq

NWORKERS = 4  # Số lượng Worker

def producer():
    context = zmq.Context()
    socket = context.socket(zmq.PUSH)  
    socket.bind("tcp://127.0.0.1:12345")  
    print("Producer đã khởi động...")

    # Chờ các Worker kết nối đầy đủ
    time.sleep(2)

    while True:
        workload = random.randint(1, 100)  
        print(f"Producer gửi công việc: {workload}")
        socket.send(pickle.dumps(workload))  
        time.sleep(workload / NWORKERS)  

def worker(id):
    context = zmq.Context()
    socket = context.socket(zmq.PULL)
    socket.connect("tcp://localhost:12345")
    
    print(f"Worker {id} đã kết nối với Producer")
    
    # Chờ một chút trước khi bắt đầu nhận công việc
    time.sleep(1)

    while True:
        work = pickle.loads(socket.recv())  
        print(f"Worker {id} nhận công việc: {work}")  
        time.sleep(work)  

if __name__ == "__main__":
    print("Bắt đầu chương trình...")
    
    producer_process = Process(target=producer)
    producer_process.start()

    worker_processes = []
    for i in range(NWORKERS):
        p = Process(target=worker, args=(i,))
        worker_processes.append(p)
        p.start()

    print("Chương trình chạy trong 10 giây...")
    time.sleep(10)  
    
    print("Dừng Producer và tất cả Worker.")
    producer_process.terminate()
    for p in worker_processes:
        p.terminate()
    
    print("Hoàn thành.")
