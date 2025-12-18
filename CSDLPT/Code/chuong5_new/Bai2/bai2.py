import random
import time

class Process:
    def __init__(self, pid):
        self.pid = pid
        self.alive = True

    def start_election(self, processes):
        print(f"\nProcess {self.pid} starts an election.")
        higher = [p for p in processes if p.pid > self.pid and p.alive]
        if not higher:
            print(f"Process {self.pid} becomes the new leader.")
            return self.pid
        else:
            for p in higher:
                print(f"Process {self.pid} sends election message to Process {p.pid}")
            # Chờ phản hồi từ tiến trình lớn hơn
            responder = higher[0]  # chỉ cần một tiến trình phản hồi là được
            return responder.start_election(processes)

def simulate_bully(N):
    processes = [Process(pid) for pid in range(1, N + 1)]
    leader = max(p.pid for p in processes)
    print(f"Initial leader is Process {leader}")

    while True:
        time.sleep(2)
        if random.random() < 0.3:  # xác suất leader chết
            for p in processes:
                if p.pid == leader:
                    p.alive = False
                    print(f"\nLeader Process {leader} has crashed.")
                    break
            alive = [p for p in processes if p.alive]
            if not alive:
                print("All processes are dead.")
                break
            new_leader = random.choice(alive).start_election(processes)
            leader = new_leader
            print(f"New leader elected: Process {leader}")

simulate_bully(5)
