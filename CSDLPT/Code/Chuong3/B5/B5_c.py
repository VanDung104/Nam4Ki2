import multiprocessing

def child_process(pipe1, pipe2):
    parent_end1, child_end1 = pipe1  # Cha → Con (Pipe 1)
    parent_end2, child_end2 = pipe2  # Con → Cha (Pipe 2)

    parent_end1.close()  # Đóng đầu cha trong tiến trình con
    parent_end2.close()  # Đóng đầu cha trong tiến trình con

    while True:
        # Nhận dữ liệu từ cha
        message = child_end1.recv()
        print(f"[Con] Nhận được từ Cha: {message}")
        
        if message == "quit":
            print("[Con] Đã nhận lệnh kết thúc.")
            break  # Dừng vòng lặp khi nhận lệnh "quit"

        # Phản hồi lại cha
        response = f"Con đã nhận: '{message}' và phản hồi lại"
        child_end2.send(response)

    child_end1.close()
    child_end2.close()

if __name__ == "__main__":
    # Tạo hai pipe: Pipe 1 (Cha → Con) và Pipe 2 (Con → Cha)
    parent_end1, child_end1 = multiprocessing.Pipe()  # Pipe 1
    parent_end2, child_end2 = multiprocessing.Pipe()  # Pipe 2

    # Tạo tiến trình con và truyền hai pipe vào
    process = multiprocessing.Process(
        target=child_process, args=((parent_end1, child_end1), (parent_end2, child_end2))
    )

    # Khởi động tiến trình con
    process.start()

    # Đóng đầu con của các pipe trong tiến trình cha
    child_end1.close()  
    child_end2.close()  # Đảm bảo rằng đầu con của cả hai pipe được đóng trong tiến trình cha

    # Giao tiếp giữa cha và con
    for i in range(3):
        user_input = input(f"[Cha] Nhập thông điệp gửi Con (Lần {i+1}): ")
        parent_end1.send(user_input)  # Gửi dữ liệu từ cha cho con

        # Nhận phản hồi từ con
        reply = parent_end2.recv()
        print(f"[Cha] Nhận phản hồi từ Con: {reply}")

    # Gửi lệnh kết thúc (quit) cho con
    parent_end1.send("quit")
    print("[Cha] Đã gửi lệnh kết thúc.")

    parent_end1.close()
    parent_end2.close()

    # Đợi tiến trình con kết thúc
    process.join()
