# Nhiều tiến trình con gửi dữ liệu về tiến trình cha
import multiprocessing
import time

def child_process(pipe, name):
    time.sleep(1)  # Mô phỏng độ trễ
    pipe.send(f"Dữ liệu từ {name}")
    pipe.close()

if __name__ == "__main__":
    parent_end, child_end = multiprocessing.Pipe()
    
    processes = []
    for i in range(3):  # Tạo 3 tiến trình con
        p = multiprocessing.Process(target=child_process, args=(child_end, f"Con {i+1}"))
        processes.append(p)
        p.start()

    child_end.close()  # Đóng đầu ghi của con trong cha

    for _ in range(3):  # Nhận dữ liệu từ các con
        message = parent_end.recv()
        print(f"Cha nhận được: {message}")

    for p in processes:
        p.join()
