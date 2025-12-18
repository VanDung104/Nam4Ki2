class VectorClockProcess:
    def __init__(self, pid, total):
        self.pid = pid
        self.clock = [0] * total
        self.total = total

    def internal_event(self):
        self.clock[self.pid] += 1
        print(f"[P{self.pid}] Internal event -> Clock = {self.clock}")

    def send(self, receiver):
        self.clock[self.pid] += 1
        print(f"[P{self.pid}] Sends message to P{receiver.pid} with clock {self.clock}")
        receiver.receive(self.clock.copy())

    def receive(self, incoming_clock):
        for i in range(self.total):
            self.clock[i] = max(self.clock[i], incoming_clock[i])
        self.clock[self.pid] += 1
        print(f"[P{self.pid}] Received message -> Updated clock = {self.clock}")


# Mô phỏng 3 tiến trình
N = 3
p0 = VectorClockProcess(0, N)
p1 = VectorClockProcess(1, N)
p2 = VectorClockProcess(2, N)

# Các sự kiện
p0.internal_event()
p0.send(p1)
p1.send(p2)
p2.internal_event()
p2.send(p0)
