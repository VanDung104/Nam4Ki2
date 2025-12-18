import multiprocessing

def child_process(pipe):
    pipe.send("Dữ liệu từ con gửi cha")  # Gửi dữ liệu qua pipe
    pipe.close()  # Đóng pipe sau khi gửi xong

if __name__ == "__main__":
    parent_end, child_end = multiprocessing.Pipe()
    p = multiprocessing.Process(target=child_process, args=(child_end,))
    
    p.start()
    child_end.close()  # Đóng đầu ghi của con trong tiến trình cha

    message = parent_end.recv()  # Nhận dữ liệu từ pipe
    print(f"Tiến trình cha nhận được: {message}")

    p.join()
