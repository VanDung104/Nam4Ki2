import socket
import threading
import time
import random
from collections import defaultdict

# Cấu hình các máy chủ
SERVERS = {
    "root": {"port": 5300, "sub_servers": ["com"]},
    "com": {"port": 5301, "sub_servers": ["example.com", "test.com"]},
    "example.com": {"port": 5302, "sub_servers": []},
    "test.com": {"port": 5303, "sub_servers": []},
}

# Dữ liệu DNS mẫu cho mỗi máy chủ
DNS_DATA = {
    "root": {
        "com": {"type": "NS", "value": "com"},
    },
    "com": {
        "example.com": {"type": "NS", "value": "example.com"},
        "test.com": {"type": "NS", "value": "test.com"},
    },
    "example.com": {
        "www.example.com": {"type": "A", "value": "192.0.2.1"},
        "mail.example.com": {"type": "A", "value": "192.0.2.2"},
    },
    "test.com": {
        "www.test.com": {"type": "A", "value": "203.0.113.1"},
        "api.test.com": {"type": "A", "value": "203.0.113.2"},
    },
}

# Bộ nhớ đệm (cache) cho mỗi máy chủ
CACHES = defaultdict(dict)

# Timeout và máy chủ thay thế
SERVER_TIMEOUT = 2  # giây
ALT_SERVERS = {
    "example.com": ["example.com", "example-backup.com"],
    "test.com": ["test.com", "test-backup.com"],
}

class DNSServer:
    def __init__(self, domain):
        self.domain = domain
        self.port = SERVERS[domain]["port"]
        self.sub_servers = SERVERS[domain]["sub_servers"]
        self.cache = CACHES[domain]
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(('localhost', self.port))
        print(f"Máy chủ {domain} đã khởi động trên cổng {self.port}")

    def handle_query(self, query, client_addr):
        print(f"{self.domain} nhận truy vấn: {query}")

        if query in self.cache:
            print(f"{self.domain} trả lời từ bộ nhớ đệm: {query}")
            self.socket.sendto(str(self.cache[query]).encode(), client_addr)
            return

        if query in DNS_DATA[self.domain]:
            record = DNS_DATA[self.domain][query]
            self.cache[query] = record
            print(f"{self.domain} trả lời từ dữ liệu cục bộ: {query}")
            self.socket.sendto(str(record).encode(), client_addr)
            return

        parts = query.split('.')
        possible_sub = None
        for sub in self.sub_servers:
            if query.endswith(sub):
                possible_sub = sub
                break

        if possible_sub:
            print(f"{self.domain} chuyển tiếp truy vấn đến {possible_sub}")
            ns_record = DNS_DATA[self.domain].get(possible_sub, {})

            if ns_record:
                try:
                    alt_servers = ALT_SERVERS.get(possible_sub, [possible_sub])

                    for server in alt_servers:
                        try:
                            result = self.forward_query(query, server)
                            if result:
                                self.cache[query] = result
                                self.socket.sendto(str(result).encode(), client_addr)
                                return
                        except socket.timeout:
                            print(f"Hết thời gian khi truy vấn {server}, thử tiếp...")
                            continue

                    error_msg = {"error": f"Tất cả các máy chủ cho {possible_sub} đều hết thời gian phản hồi"}
                    self.socket.sendto(str(error_msg).encode(), client_addr)
                except Exception as e:
                    error_msg = {"error": str(e)}
                    self.socket.sendto(str(error_msg).encode(), client_addr)
            else:
                error_msg = {"error": f"Không có bản ghi NS cho {possible_sub}"}
                self.socket.sendto(str(error_msg).encode(), client_addr)
        else:
            error_msg = {"error": f"Không tìm thấy bản ghi cho {query} tại {self.domain}"}
            self.socket.sendto(str(error_msg).encode(), client_addr)

    def forward_query(self, query, target_domain):
        target_port = SERVERS[target_domain]["port"]
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(SERVER_TIMEOUT)
        s.sendto(query.encode(), ('localhost', target_port))
        data, _ = s.recvfrom(1024)
        s.close()
        return eval(data.decode())

    def start(self):
        while True:
            data, addr = self.socket.recvfrom(1024)
            query = data.decode().strip()
            threading.Thread(target=self.handle_query, args=(query, addr)).start()

def start_servers():
    servers = []
    for domain in SERVERS:
        server = DNSServer(domain)
        t = threading.Thread(target=server.start, daemon=True)  # <- Thêm daemon=True
        t.start()
        servers.append(server)
    return servers

def interactive_query():
    print("Mô phỏng hệ thống phân giải tên miền DNS phân tán")
    print("Các tên miền có thể truy vấn: www.example.com, mail.example.com, www.test.com, api.test.com")
    print("Nhập 'quit' để thoát")

    while True:
        query = input("\nNhập tên miền cần phân giải: ").strip()
        if query.lower() == 'quit':
            break

        if not query:
            continue

        try:
            result = query_dns(query, "root")
            print("\nLộ trình phân giải:")
            for step in result['path']:
                print(f" - {step}")
            print(f"\nKết quả cuối cùng: {result['data']}")
        except Exception as e:
            print(f"Lỗi: {e}")

def query_dns(query, start_server):
    path = []
    current_server = start_server
    visited_servers = set()

    while True:
        if current_server in visited_servers:
            raise Exception("Phát hiện vòng lặp trong phân giải")
        visited_servers.add(current_server)

        path.append(f"Gửi truy vấn đến {current_server} cho {query}")

        port = SERVERS[current_server]["port"]
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(SERVER_TIMEOUT)

        try:
            s.sendto(query.encode(), ('localhost', port))
            data, _ = s.recvfrom(1024)
            response = eval(data.decode())
        finally:
            s.close()

        if 'error' in response:
            return {'path': path, 'data': response}

        path.append(f"Nhận phản hồi: {response} từ {current_server}")

        if response['type'] == 'A':
            return {'path': path, 'data': response}
        elif response['type'] == 'NS':
            current_server = response['value']
        else:
            raise Exception(f"Loại bản ghi không xác định: {response['type']}")

if __name__ == "__main__":
    servers = start_servers()
    time.sleep(1)
    try:
        interactive_query()
    except KeyboardInterrupt:
        print("\nTắt hệ thống...")
        exit(0)
