import heapq
import threading
import time

class LamportClock:
    def __init__(self):
        self.clock = 0
        self.lock = threading.Lock()
    
    def tick(self):
        with self.lock:
            self.clock += 1
            return self.clock
    
    def update(self, received_time):
        with self.lock:
            self.clock = max(self.clock, received_time) + 1
            return self.clock

class Process:
    def __init__(self, pid, lamport_clock, processes):
        self.pid = pid
        self.clock = lamport_clock
        self.queue = []
        self.processes = processes
        self.acks_received = 0
    
    def request_access(self):
        timestamp = self.clock.tick()
        print(f"Process {self.pid} requests access at time {timestamp}")
        self.acks_received = 0
        for process in self.processes:
            if process.pid != self.pid:
                process.receive_ack(self.pid, timestamp)
    
    def receive_ack(self, sender_pid, received_time):
        self.clock.update(received_time)
        print(f"Process {self.pid} received ACK from Process {sender_pid} at time {self.clock.clock}")
        self.acks_received += 1
        
        if self.acks_received == len(self.processes) - 1:
            self.enter_queue()
    
    def enter_queue(self):
        timestamp = self.clock.tick()
        heapq.heappush(self.queue, (timestamp, self.pid))
        print(f"Process {self.pid} enters queue at time {timestamp}")
    
    def release_access(self):
        timestamp = self.clock.tick()
        print(f"Process {self.pid} releases access at time {timestamp}")
        for process in self.processes:
            if process.pid != self.pid:
                process.remove_from_queue(self.pid)
    
    def remove_from_queue(self, pid):
        self.queue = [(t, p) for (t, p) in self.queue if p != pid]
        heapq.heapify(self.queue)
        print(f"Process {self.pid} removed Process {pid} from queue")

if __name__ == "__main__":
    lamport_clock = LamportClock()
    
    process1 = Process(1, lamport_clock, [])
    process2 = Process(2, lamport_clock, [])
    process3 = Process(3, lamport_clock, [])
    
    processes = [process1, process2, process3]
    for process in processes:
        process.processes = processes
    
    # Khởi tạo queue với một tiến trình đang chạy sẵn
    process1.enter_queue()
    print("Process 1 is already running.")
    
    time.sleep(0.5)
    process2.request_access()
    time.sleep(0.5)
    process3.request_access()
    
    time.sleep(1)
    process1.release_access()
    time.sleep(1)
    process2.release_access()
