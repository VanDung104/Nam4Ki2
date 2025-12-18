import logging
import time
import threading

N = 5          
ROUNDS = 3   

logging.basicConfig(
    level=logging.INFO,
    # format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
class TokenRingController:
    def __init__(self):
        self.token_holder = 0
        self.lock = threading.Lock()
        self.round = 1
        self.done = False

class TokenRingNode(threading.Thread):
    def __init__(self, node_id, controller):
        super().__init__()
        self.node_id = node_id
        self.controller = controller

    def run(self):
        while not self.controller.done:
            with self.controller.lock:
                if self.controller.token_holder == self.node_id:
                    logging.info(f"Process {self.node_id + 1} nhận token")
                    logging.info(f"Process {self.node_id + 1}: Tôi đang giữ token")
                    time.sleep(1)

                    next_id = (self.node_id + 1) % N
                    logging.info(f"Process {self.node_id + 1} chuyển token cho Process {next_id + 1}")

                    if next_id == 0:
                        logging.info(f"Hoàn thành vòng {self.controller.round}/{ROUNDS}")
                        self.controller.round += 1
                        if self.controller.round > ROUNDS:
                            self.controller.done = True

                    self.controller.token_holder = next_id
            time.sleep(0.1)

def main():
    logging.info("Bắt đầu truyền token")
    controller = TokenRingController()
    nodes = [TokenRingNode(i, controller) for i in range(N)]

    for node in nodes:
        node.start()

    for node in nodes:
        node.join() 

    logging.info("Mô phỏng Token Ring kết thúc")

if __name__ == "__main__":
    main()
