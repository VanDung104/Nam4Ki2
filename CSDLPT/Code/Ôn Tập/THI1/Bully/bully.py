import time
from threading import Thread, Lock
from queue import Queue

# Sử dụng queue để đồng bộ hóa log
log_queue = Queue()
print_lock = Lock()

class Process:
    def __init__(self, pid, all_processes):
        self.pid = pid
        self.all_processes = all_processes
        self.leader = None
        self.active = True
        self.lock = Lock()
        self.election_in_progress = False
    
    def log(self, message):
        log_queue.put(f"[{time.strftime('%H:%M:%S')}] P{self.pid}: {message}")
    
    def send_election(self):
        with self.lock:
            if self.election_in_progress or not self.active:
                return
            self.election_in_progress = True
            
        self.log("Khởi xướng bầu chọn")
        higher_processes = [p for p in self.all_processes if p.pid > self.pid and p.active]
        
        if not higher_processes:
            self.declare_leader()
            return
        
        responses = []
        for process in higher_processes:
            if process.receive_election(self.pid):
                responses.append(True)
                time.sleep(0.01)  # Thêm delay nhỏ
        
        if not responses:
            self.declare_leader()
            
        with self.lock:
            self.election_in_progress = False
    
    def receive_election(self, sender_pid):
        if not self.active:
            return False
        
        self.log(f"Nhận election message từ P{sender_pid}")
        # Trả lời OK và tự khởi xướng bầu chọn
        Thread(target=self.send_election).start()
        return True
    
    def declare_leader(self):
        with self.lock:
            if self.leader == self.pid:
                return
                
            self.log("Tuyên bố là leader mới!")
            self.leader = self.pid
            # Thông báo cho các tiến trình khác
            for process in self.all_processes:
                if process.pid != self.pid and process.active:
                    process.receive_leader(self.pid)
    
    def receive_leader(self, leader_pid):
        with self.lock:
            if self.leader == leader_pid:
                return
                
            self.log(f"Nhận leader mới là P{leader_pid}")
            self.leader = leader_pid
    
    def fail(self):
        with self.lock:
            if not self.active:
                return
                
            self.log("Bị lỗi!")
            self.active = False
    
    def check_leader(self):
        if self.leader and self.leader != self.pid:
            leader_process = next((p for p in self.all_processes if p.pid == self.leader), None)
            if not leader_process or not leader_process.active:
                self.log(f"Phát hiện leader P{self.leader} bị lỗi")
                self.send_election()

def logger():
    while True:
        message = log_queue.get()
        with print_lock:
            print(message)
        log_queue.task_done()

def simulate():
    # Bật logger
    Thread(target=logger, daemon=True).start()
    
    log_queue.put(f"[{time.strftime('%H:%M:%S')}] === Bắt đầu mô phỏng ===")
    
    # Tạo 5 tiến trình
    processes = [Process(i+1, []) for i in range(5)]
    for p in processes:
        p.all_processes = processes
    
    # Đặt P5 là leader ban đầu
    for p in processes:
        p.leader = 5
    
    log_queue.put(f"[{time.strftime('%H:%M:%S')}] === Trạng thái ban đầu ===")
    log_queue.put(f"[{time.strftime('%H:%M:%S')}] Leader hiện tại: P5\n")
    
    # Mô phỏng P5 bị lỗi sau 3 giây
    time.sleep(3)
    processes[-1].fail()
    
    # Các tiến trình khác phát hiện leader bị lỗi
    time.sleep(1)
    log_queue.put(f"\n[{time.strftime('%H:%M:%S')}] === Các process bắt đầu kiểm tra leader ===")
    for p in processes[:-1]:
        p.check_leader()
    
    # Đợi quá trình bầu chọn hoàn tất
    time.sleep(2)
    
    # Kiểm tra leader mới
    new_leader = None
    for p in processes:
        if p.active and p.leader == p.pid:
            new_leader = p.pid
            break
    
    log_queue.put(f"\n[{time.strftime('%H:%M:%S')}] === Kết quả ===")
    log_queue.put(f"[{time.strftime('%H:%M:%S')}] Leader mới là P{new_leader}")
    
    # Đợi log hoàn tất
    time.sleep(1)

if __name__ == "__main__":
    simulate()