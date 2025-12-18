import threading
import time
import random

n = 10  # Số lượng luồng
k = 3   # Số luồng tối đa chạy đồng thời

# c) Mô phỏng một hệ thống quản lý truy cập phòng họp, 
# chỉ cho phép tối đa N người vào cùng lúc. Khi phòng họp đã đầy, các nhân viên khác phải chờ đến lượt.
meeting_room_capacity = 5
meeting_room = threading.Semaphore(meeting_room_capacity)

def enter_meeting_room(user_id):
    with meeting_room:
        print(f"Người dùng {user_id + 1} đã đi vào phòng.")
        time.sleep(random.uniform(2, 4))
        print(f"Người dùng {user_id + 1} đã ròi khỏi phòng.")

threads = []
for i in range(n):
    t = threading.Thread(target=enter_meeting_room, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
