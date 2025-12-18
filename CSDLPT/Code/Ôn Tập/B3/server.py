import socket
import pickle
import struct
import concurrent.futures

WORKER_NODES = [
    ("127.0.0.1", 5001),  # Worker 1
    ("127.0.0.1", 5002),  # Worker 2
    ("127.0.0.1", 5003),  # Worker 3
]

def split_list(numbers, num_workers):
    """Chia danh sách thành các phần bằng nhau"""
    chunk_size = (len(numbers) + num_workers - 1) // num_workers
    return [numbers[i*chunk_size:(i+1)*chunk_size] for i in range(num_workers)]

def send_to_worker(worker_ip, port, numbers):
    """Gửi dữ liệu đến worker và nhận kết quả"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.settimeout(10)
            client.connect((worker_ip, port))
            
            data = pickle.dumps(numbers)
            client.sendall(struct.pack(">I", len(data)) + data)
            
            result_size = struct.unpack(">I", client.recv(4))[0]
            result = b''
            while len(result) < result_size:
                packet = client.recv(result_size - len(result))
                if not packet:
                    break
                result += packet
                
            return pickle.loads(result)
    except Exception as e:
        print(f"Lỗi khi giao tiếp với {worker_ip}:{port}: {str(e)}")
        return []  # Trả về list rỗng nếu có lỗi

def find_primes_distributed(numbers):
    """Phân tán kiểm tra số nguyên tố"""
    chunks = split_list(numbers, len(WORKER_NODES))
    
    primes = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for (worker_ip, port), chunk in zip(WORKER_NODES, chunks):
            print(f"Gửi {len(chunk)} số đến {worker_ip}:{port}")
            futures.append(executor.submit(send_to_worker, worker_ip, port, chunk))
        
        for future in concurrent.futures.as_completed(futures):
            primes.extend(future.result())
    
    return sorted(primes)

if __name__ == "__main__":
    # Ví dụ kiểm tra các số từ 1 đến 1000
    numbers = list(range(1, 14))
    primes = find_primes_distributed(numbers)
    print(f"Tìm thấy {len(primes)} số nguyên tố:")
    print(primes)