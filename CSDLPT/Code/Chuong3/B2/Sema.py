import threading
import time

semaphore = threading.Semaphore(1)  # Chỉ cho phép 1 tiến trình vào vùng quan trọng

def process(name):
    print(f"{name} đang chờ tài nguyên...")
    with semaphore:
        print(f"{name} đang sử dụng tài nguyên")
        time.sleep(2)
        print(f"{name} đã hoàn thành và giải phóng tài nguyên")

threads = [threading.Thread(target=process, args=(f"Process {i+1}",)) for i in range(3)]

for t in threads:
    t.start()

for t in threads:
    t.join()
