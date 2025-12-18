import threading
import time

# Tạo hai khóa (locks) cho tài nguyên 1 và 2
resource_1 = threading.Lock()
resource_2 = threading.Lock()
resource_3 = threading.Lock()

def process_a():
    print("Process A đang cố gắng lấy Resource 1...")
    with resource_1:
        print("Process A đã lấy Resource 1")
        time.sleep(1)  # Giả lập công việc
        
        print("Process A đang cố gắng lấy Resource 2...")
        acquired = resource_2.acquire(timeout=2)  # Sử dụng timeout
        if acquired:
            print("Process A đã lấy Resource 2")
            resource_2.release()
        else:
            print("Process A không lấy được Resource 2, tránh Deadlock!")

def process_b():
    print("Process B đang cố gắng lấy Resource 2...")
    with resource_2:
        print("Process B đã lấy Resource 2")
        time.sleep(1)  # Giả lập công việc
        
        print("Process B đang cố gắng lấy Resource 3...")
        acquired = resource_3.acquire(timeout=2)  # Sử dụng timeout
        if acquired:
            print("Process B đã lấy Resource 3")
            resource_3.release()
        else:
            print("Process B không lấy được Resource 3, tránh Deadlock!")

def process_c():
    print("Process C đang cố gắng lấy Resource 3...")
    with resource_3:
        print("Process C đã lấy Resource 3")
        time.sleep(1)  # Giả lập công việc
        
        print("Process C đang cố gắng lấy Resource 1...")
        acquired = resource_1.acquire(timeout=2)  # Sử dụng timeout
        if acquired:
            print("Process C đã lấy Resource 1")
            resource_1.release()
        else:
            print("Process C không lấy được Resource 1, tránh Deadlock!")
# Tạo và chạy hai luồng (threads)
thread_a = threading.Thread(target=process_a)
thread_b = threading.Thread(target=process_b)
thread_c = threading.Thread(target=process_c)

thread_a.start()
thread_b.start()
thread_c.start()

thread_a.join()
thread_b.join()
thread_c.join()

print("Chương trình kết thúc!")
