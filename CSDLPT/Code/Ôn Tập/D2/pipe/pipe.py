import os
import sys
from multiprocessing import Process, Pipe

def child_process(conn):
    while True:
        data = conn.recv()  # Nhận dữ liệu từ pipe
        if data.lower() == "exit":
            break
        # Xử lý dữ liệu (ví dụ: viết hoa toàn bộ)
        processed_data = data.upper()
        conn.send(processed_data)  # Gửi kết quả về
    conn.close()
    sys.exit(0)

def parent_process():
    parent_conn, child_conn = Pipe()  # Tạo pipe
    
    p = Process(target=child_process, args=(child_conn,))
    p.start()
    
    print("Nhập văn bản (gõ 'exit' để kết thúc):")
    while True:
        user_input = input("> ")
        # Gửi dữ liệu tới tiến trình con
        parent_conn.send(user_input)
        
        if user_input.lower() == "exit":
            break
            
        # Nhận kết quả từ tiến trình con
        processed_data = parent_conn.recv()
        print("Kết quả:", processed_data)
    
    parent_conn.close()
    p.join()  # Chờ tiến trình con kết thúc

if __name__ == "__main__":
    parent_process()