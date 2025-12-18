import threading
import time

# a) Mô phỏng race condition
counter = 0
def increment_without_lock():
    global counter
    temp = counter
    time.sleep(0.0001)  # Giả lập độ trễ
    counter = temp + 1

def run_threads_without_lock():
    global counter
    counter = 0
    threads = [threading.Thread(target=increment_without_lock) for _ in range(100)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print(f"Counter without lock: {counter}")

# b) Giải quyết race condition bằng Lock
lock = threading.Lock()
def increment_with_lock():
    global counter
    with lock:
        temp = counter
        time.sleep(0.01)
        counter = temp + 1

def run_threads_with_lock():
    global counter
    counter = 0
    threads = [threading.Thread(target=increment_with_lock) for _ in range(100)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print(f"Counter with lock: {counter}")

# c) Dùng RLock để tránh Deadlock
rlock = threading.RLock()
def increment_with_rlock():
    global counter
    with rlock:
        temp = counter
        time.sleep(0.01)
        counter = temp + 1

def run_threads_with_rlock():
    global counter
    counter = 0
    threads = [threading.Thread(target=increment_with_rlock) for _ in range(100)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print(f"Counter with RLock: {counter}")

# Chạy các thử nghiệm
run_threads_without_lock()
run_threads_with_lock()
run_threads_with_rlock()
