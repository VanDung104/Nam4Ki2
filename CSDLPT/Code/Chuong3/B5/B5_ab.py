import multiprocessing

def child_process(pipe1, pipe2):
    parent_end1, child_end1 = pipe1
    parent_end2, child_end2 = pipe2

    parent_end1.close()  # Đóng đầu cha (để con chỉ nhận dữ liệu từ pipe1)
    parent_end2.close()  # Đóng đầu cha (để con chỉ gửi dữ liệu qua pipe2)

    # Nhận dữ liệu từ cha
    message = child_end1.recv()
    print(f"[Con] Nhận được từ Cha: {message}")

    # Phản hồi lại cha qua pipe2
    response = f"Con đã nhận: '{message}' và phản hồi lại"
    child_end2.send(response)

    child_end1.close()  # Đóng đầu con của pipe1
    child_end2.close()  # Đóng đầu con của pipe2

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

    # Nhập dữ liệu từ người dùng và gửi qua pipe1 (Cha → Con)
    user_input = input("[Cha] Nhập thông điệp gửi Con: ")
    parent_end1.send(user_input)

    # Nhận phản hồi từ con qua pipe2 (Con → Cha)
    reply = parent_end2.recv()
    print(f"[Cha] Nhận phản hồi từ Con: {reply}")

    # Đóng đầu cha của các pipe trong tiến trình cha sau khi đã nhận phản hồi
    parent_end1.close()
    parent_end2.close()

    # Đợi tiến trình con kết thúc
    process.join()
