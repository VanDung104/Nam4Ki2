import multiprocessing
import time
import random
from datetime import datetime

MAX_ACCESS = 2   # Số tiến trình được truy cập tài nguyên cùng lúc
NUM_PROCESSES = 5  # Tổng số tiến trình
TIMEOUT = 3      # Timeout nếu chờ quá lâu

LOG_FILE = 'D://Nam4Ki2//CSDLPT//Code//Ôn Tập//De3//sema//access_log.txt'

def log(message):
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        now = datetime.now().strftime("%H:%M:%S")
        f.write(f"[{now}] {message}\n")
    print(f"[{now}] {message}")

def access_resource(sem: multiprocessing.Semaphore, proc_id: int):
    while True:
        log(f"Tiến trình {proc_id} đang xin quyền truy cập...")

        acquired = sem.acquire(timeout=TIMEOUT)
        if acquired:
            try:
                log(f"Tiến trình {proc_id} ĐƯỢC quyền truy cập.")
                time_to_sleep = random.randint(2, 5)
                time.sleep(time_to_sleep)
                log(f"Tiến trình {proc_id} hoàn thành sau {time_to_sleep}s.")
            finally:
                sem.release()
                log(f"Tiến trình {proc_id} đã THOÁT tài nguyên.")
                break
        else:
            log(f"Tiến trình {proc_id} TIMEOUT. Thử lại sau...")
            time.sleep(1)  # đợi 1s rồi thử lại

if __name__ == '__main__':
    open(LOG_FILE, 'w').close()  # Xóa log cũ

    sem = multiprocessing.Semaphore(MAX_ACCESS)
    processes = []

    for i in range(NUM_PROCESSES):
        p = multiprocessing.Process(target=access_resource, args=(sem, i + 1))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    log("Tất cả tiến trình đã hoàn thành.")
