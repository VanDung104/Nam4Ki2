import socket
import pickle
import struct

# Danh sách IP các máy Worker
WORKER_NODES = [
    ("127.0.0.1", 5001),  # Worker 1
    ("127.0.0.1", 5002),  # Worker 2
]

def split_list(numbers, num_workers):
    """Chia danh sách thành các phần nhỏ để gửi cho các Worker."""
    chunk_size = len(numbers) // num_workers
    chunks = [numbers[i * chunk_size: (i + 1) * chunk_size] for i in range(num_workers)]
    
    # Gộp phần dư vào nhóm cuối cùng
    remainder = numbers[num_workers * chunk_size:]
    if remainder:
        chunks[-1].extend(remainder)
    
    return chunks

def send_to_worker(worker_ip, port, numbers):
    """Gửi dữ liệu đến Worker và nhận kết quả."""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((worker_ip, port))

    data = pickle.dumps(numbers)
    data_size = struct.pack(">I", len(data))  # Đóng gói kích thước

    client.sendall(data_size)  # Gửi kích thước trước
    client.sendall(data)  # Gửi dữ liệu chính

    result_size = struct.unpack(">I", client.recv(4))[0]  # Nhận kích thước kết quả
    result = pickle.loads(client.recv(result_size))  # Nhận kết quả tổng

    client.close()
    return result

def distributed_server():
    """Chia danh sách và gửi đến các Worker."""
    numbers = list(range(1, 10**6 + 1))  # Danh sách 1 triệu số
    chunks = split_list(numbers, len(WORKER_NODES))

    total_sum = 0
    for i, (worker_ip, port) in enumerate(WORKER_NODES):
        print(f"Gửi {len(chunks[i])} số đến Worker {i+1} ({worker_ip}:{port})...")
        total_sum += send_to_worker(worker_ip, port, chunks[i])

    print(f"Tổng cuối cùng: {total_sum}")

if __name__ == "__main__":
    distributed_server()
