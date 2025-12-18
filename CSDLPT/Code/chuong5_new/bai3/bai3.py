import random
import time

class Process:
    def __init__(self, pid):
        self.pid = pid
        self.alive = True

def send_election(start_index, processes):
    N = len(processes)
    election_msg = []
    index = start_index
    print(f"\n[+] Process {processes[index].pid} starts an election.")

    while True:
        if processes[index].alive:
            election_msg.append(processes[index].pid)
            print(f"[>] Election message passed through Process {processes[index].pid}")
        index = (index + 1) % N
        if index == start_index:
            break

    new_leader = max(election_msg)
    print(f"[✔] Election completed. New leader is Process {new_leader}")
    announce_leader(start_index, processes, new_leader)
    return new_leader

def announce_leader(start_index, processes, leader_pid):
    N = len(processes)
    index = start_index
    print(f"[+] Announcing new leader {leader_pid} to all processes:")
    while True:
        if processes[index].alive:
            print(f"[!] Process {processes[index].pid} is informed: Leader is {leader_pid}")
        index = (index + 1) % N
        if index == start_index:
            break

def simulate_ring(N):
    processes = [Process(pid) for pid in range(1, N + 1)]
    leader = max(p.pid for p in processes)
    print(f"[*] Initial leader is Process {leader}")

    while True:
        time.sleep(2)
        if random.random() < 0.3:  # xác suất leader lỗi
            for p in processes:
                if p.pid == leader:
                    p.alive = False
                    print(f"\n[!] Leader Process {leader} has crashed.")
                    break
            alive_indexes = [i for i, p in enumerate(processes) if p.alive]
            if not alive_indexes:
                print("[X] All processes are dead.")
                break
            start = random.choice(alive_indexes)
            leader = send_election(start, processes)

simulate_ring(5)
