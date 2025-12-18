import time
import random

class Client:
    def __init__(self, client_id, server):
        self.client_id = client_id
        self.server = server
        self.has_lock = False
    
    def acquire_lock(self):
        print(f"Client {self.client_id} requesting lock")
        granted = self.server.handle_request(self.client_id)
        
        if granted:
            self.has_lock = True
            print(f"Client {self.client_id} acquired lock immediately")
            return True
        else:
            print(f"Client {self.client_id} added to queue, waiting...")
            while not self.has_lock:
                # Trong thực tế, đây sẽ là cơ chế callback hoặc notification
                time.sleep(1)
                # Kiểm tra xem có phải là client tiếp theo không
                if self.server.lock_holder == self.client_id:
                    self.has_lock = True
                    print(f"Client {self.client_id} acquired lock after waiting")
                    return True
            return False
    
    def release_lock(self):
        if self.has_lock:
            print(f"Client {self.client_id} releasing lock")
            next_client = self.server.handle_release(self.client_id)
            self.has_lock = False
            if next_client:
                print(f"Lock granted to next client: {next_client}")
            else:
                print("Lock released, no waiting clients")
            return True
        return False
    
    def do_work(self):
        # Mô phỏng công việc khi có lock
        work_time = random.uniform(1, 3)
        print(f"Client {self.client_id} doing work for {work_time:.2f} seconds")
        time.sleep(work_time)

# Tạo các client
lock_server = ('localhost', 65432)

client1 = Client(1, lock_server)
client2 = Client(2, lock_server)
client3 = Client(3, lock_server)