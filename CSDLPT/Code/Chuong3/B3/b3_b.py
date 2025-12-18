import threading
import time
import random

n = 10
# b) Ghi vào file với Semaphore để tránh xung đột
file_lock = threading.Semaphore(1)
def write_to_file(user_id):
    with file_lock:
        with open("D:\\Nam4Ki2\\CSDLPT\\Code\\Chuong3\\B3\\output.txt", "a", encoding="utf-8") as f:
            f.write(f"Người dùng {user_id + 1} đang viết vào file.\n")
            time.sleep(random.uniform(1, 2))
            f.write(f"Người dùng {user_id + 1} đã viết xong.\n")

threads = []
for i in range(n):
    t = threading.Thread(target=write_to_file, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

