from xmlrpc.client import ServerProxy
import random
import string

def generate_random_string(length=5):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def generate_string_list(n):
    return [generate_random_string(random.randint(3, 7)) for _ in range(n)]

def input_strings_manually(n):
    print(f"Nhập {n} chuỗi:")
    return [input(f"Chuỗi {i+1}: ") for i in range(n)]

def split_data(data, n_parts):
    return [data[i::n_parts] for i in range(n_parts)]

if __name__ == "__main__":
    NUM_STRINGS = 4
    NUM_SERVERS = 3

    mode = input("Nhập thủ công (t) hay sinh ngẫu nhiên (n)? [t/n]: ").lower()
    if mode == 't':
        strings = input_strings_manually(NUM_STRINGS)
    else:
        strings = generate_string_list(NUM_STRINGS)
        print("Danh sách chuỗi được sinh tự động:")
        print(strings)

    # Chia dữ liệu cho 3 server
    server_data = split_data(strings, NUM_SERVERS)

    # Kết nối tới các server RPC
    ports = [8000, 8001, 8002]
    servers = [ServerProxy(f"http://localhost:{port}/", allow_none=True) for port in ports]

    # Gửi yêu cầu tới từng server
    results = []
    for i in range(NUM_SERVERS):
        print(f"[CLIENT] Gửi {len(server_data[i])} chuỗi đến Server {i} (port {ports[i]})")
        result = servers[i].filter_palindromes(server_data[i])
        print(f"[CLIENT] Server {i} trả về: {result}")
        results.extend(result)

    # Hiển thị kết quả tổng hợp
    print("\nCác chuỗi là Palindrome:")
    for s in results:
        print(f" - {s}")
