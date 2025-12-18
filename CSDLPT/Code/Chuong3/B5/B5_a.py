import multiprocessing
import time

def child_process(pipe):
    parent_end, child_end = pipe  # Nhận cả 2 đầu từ cha
    parent_end.close()  # Đóng đầu cha trong tiến trình con
    message = child_end.recv()  # Đọc từ pipe
    print(f"Tiến trình con nhận: {message}")

if __name__ == "__main__":
    parent_end, child_end = multiprocessing.Pipe()
    p = multiprocessing.Process(target=child_process, args=((parent_end, child_end),))
    
    p.start()
    child_end.close()  # Đóng đầu con trong tiến trình cha

    parent_end.send("Xin chào từ cha!")  # Gửi dữ liệu trước khi con đọc
    p.join()
