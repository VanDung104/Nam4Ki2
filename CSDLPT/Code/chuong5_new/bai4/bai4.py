class LamportProcess:
    def __init__(self, pid):
        self.pid = pid
        self.clock = 0

    def internal_event(self):
        self.clock += 1
        print(f"[P{self.pid}] Internal event -> Clock = {self.clock}")

    def send(self, receiver):
        self.clock += 1
        timestamp = self.clock
        print(f"[P{self.pid}] Sends message to P{receiver.pid} with timestamp {timestamp}")
        receiver.receive(timestamp)

    def receive(self, timestamp):
        self.clock = max(self.clock, timestamp) + 1
        print(f"[P{self.pid}] Received message -> Clock = {self.clock}")


# Mô phỏng
p1 = LamportProcess(1)
p2 = LamportProcess(2)

# Các sự kiện xảy ra
p1.internal_event()
p2.internal_event()
p1.send(p2)
p2.send(p1)
p1.internal_event()
