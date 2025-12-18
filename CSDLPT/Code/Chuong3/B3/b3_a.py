import threading
import time
import random

# a) Quản lý truy cập tài nguyên chung với Semaphore
def access_resource(semaphore, user_id):
    with semaphore:
        print(f"Người dùng {user_id + 1} đang truy cập.")
        time.sleep(random.uniform(1, 3))
        print(f"Người dùng {user_id + 1} đã thoát.")

n = 10  # Số lượng luồng
k = 3   # Số luồng tối đa chạy đồng thời
semaphore = threading.Semaphore(k)

threads = []
for i in range(n):
    t = threading.Thread(target=access_resource, args=(semaphore, i))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
