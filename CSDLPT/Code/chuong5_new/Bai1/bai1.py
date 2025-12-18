import threading
import socket
import json
import time
from datetime import datetime
import random

class Process:
    def __init__(self, pid, port, all_ports):
        self.pid = pid
        self.port = port
        self.all_ports = all_ports  # Danh sách cổng của tất cả các tiến trình
        self.clock = 0  # Đồng hồ Lamport
        self.requesting = False
        self.deferred = []  # Các yêu cầu bị trì hoãn
        self.replies_received = 0
        self.current_request_ts = None
        
        # Khởi tạo socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(('localhost', self.port))
        
        # Bắt đầu thread lắng nghe
        self.listener_thread = threading.Thread(target=self.listen)
        self.listener_thread.daemon = True
        self.listener_thread.start()
        
    def log(self, message):
        print(f"[Tiến trình {self.pid}][Đồng hồ {self.clock}] {message}")
        
    def update_clock(self, received_clock=None):
        if received_clock is not None:
            self.clock = max(self.clock, received_clock) + 1
        else:
            self.clock += 1
    
    def send_message(self, dest_port, message_type, **kwargs):
        self.update_clock()
        message = {
            'type': message_type,
            'sender_pid': self.pid,
            'sender_port': self.port,
            'timestamp': self.clock,
            **kwargs
        }
        self.socket.sendto(json.dumps(message).encode(), ('localhost', dest_port))
        self.log(f"Đã gửi {message_type} tới Tiến trình {self.all_ports.index(dest_port)}")
        
    def listen(self):
        while True:
            data, addr = self.socket.recvfrom(1024)
            message = json.loads(data.decode())
            self.update_clock(message['timestamp'])
            
            if message['type'] == 'REQUEST':
                self.handle_request(message)
            elif message['type'] == 'REPLY':
                self.handle_reply(message)
    
    def handle_request(self, message):
        self.log(f"Đã nhận YÊU CẦU từ Tiến trình {message['sender_pid']}")
        
        # Kiểm tra nếu mình không yêu cầu hoặc yêu cầu của người khác có độ ưu tiên cao hơn
        if not self.requesting or (
            message['timestamp'] < self.current_request_ts or 
            (message['timestamp'] == self.current_request_ts and message['sender_pid'] < self.pid)
        ):
            self.send_message(message['sender_port'], 'REPLY')
            self.log(f"Đã gửi PHẢN HỒI ngay lập tức tới Tiến trình {message['sender_pid']}")
        else:
            self.deferred.append(message)
            self.log(f"Đã hoãn YÊU CẦU từ Tiến trình {message['sender_pid']}")
    
    def handle_reply(self, message):
        self.log(f"Đã nhận PHẢN HỒI từ Tiến trình {message['sender_pid']}")
        self.replies_received += 1
        
        if self.replies_received == len(self.all_ports) - 1:
            self.enter_critical_section()
    
    def request_critical_section(self):
        self.log("Đang yêu cầu vào vùng tranh chấp")
        self.requesting = True
        self.replies_received = 0
        self.current_request_ts = self.clock
        
        for port in self.all_ports:
            if port != self.port:
                self.send_message(port, 'REQUEST')
    
    def enter_critical_section(self):
        self.log("ĐÃ VÀO VÙNG TRANH CHẤP")
        # Giả lập thực hiện công việc trong vùng tranh chấp
        time.sleep(random.uniform(1, 3))
        self.exit_critical_section()
    
    def exit_critical_section(self):
        self.log("ĐÃ RỜI VÙNG TRANH CHẤP")
        self.requesting = False
        self.current_request_ts = None
        
        # Gửi phản hồi cho các yêu cầu bị hoãn
        for deferred_req in self.deferred:
            self.send_message(deferred_req['sender_port'], 'REPLY')
            self.log(f"Đã gửi PHẢN HỒI bị hoãn tới Tiến trình {deferred_req['sender_pid']}")
        
        self.deferred = []
    
    def simulate_work(self):
        while True:
            # Giả lập thời gian làm việc bên ngoài vùng tranh chấp
            time.sleep(random.uniform(2, 5))
            self.request_critical_section()

def main():
    # Cấu hình: danh sách cổng cho các tiến trình
    N = 3  # Số lượng tiến trình
    ports = [5000 + i for i in range(N)]
    
    # Tạo các tiến trình
    processes = []
    for i in range(N):
        p = Process(i, ports[i], ports)
        processes.append(p)
    
    # Bắt đầu mô phỏng công việc
    for p in processes:
        threading.Thread(target=p.simulate_work, daemon=True).start()
    
    # Chạy vô hạn
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nĐang tắt chương trình...")

if __name__ == "__main__":
    main()