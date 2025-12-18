import time
import random

# Root Server
root_server = {
    ".com": "TLD_COM",
    ".org": "TLD_ORG",
    ".vn": "TLD_VN"
}

# TLD Servers
tld_servers = {
    "TLD_COM": {
        "example.com": "AUTH_EXAMPLE_COM",
        "shop.com": "AUTH_SHOP_COM"
    },
    "TLD_ORG": {
        "myorg.org": "AUTH_MYORG_ORG"
    }
}

# Authoritative Servers
auth_servers = {
    "AUTH_EXAMPLE_COM": {
        "www.example.com": "192.168.1.1",
        "mail.example.com": "192.168.1.2"
    },
    "AUTH_MYORG_ORG": {
        "mail.myorg.org": "10.0.0.1",
        "shop.myorg.org": "10.0.0.2"
    }
}

# Giả lập lỗi với xác suất (default 20%)
def simulate_failure(probability=0.2):
    return random.random() < probability

# Truy vấn an toàn (có thể lỗi)
def safe_lookup(server_dict, key, label="Server", fail_rate=0.2):
    if simulate_failure(fail_rate):
        print(f" {label} bị lỗi (Timeout)")
        return None
    return server_dict.get(key)

# Hàm phân giải DNS
def resolve(domain):
    print(f"\nResolving: {domain}")
    start = time.time()

    # Bước 1: lấy TLD
    parts = domain.split(".")
    if len(parts) < 2:
        return "Tên miền không hợp lệ"
    tld = "." + parts[-1]

    # Truy vấn Root Server
    t1 = time.time()
    tld_server = safe_lookup(root_server, tld, label="Root Server")
    if not tld_server:
        return f"Root Server không phản hồi hoặc không có TLD {tld} (t= {time.time() - t1:.4f}s)"
    print(f" Root → TLD: {tld_server} (t= {time.time() - t1:.4f}s)")

    # Truy vấn TLD Server
    second_level = ".".join(parts[-2:])
    t2 = time.time()
    tld_data = tld_servers.get(tld_server, {})
    auth_server = safe_lookup(tld_data, second_level, label="TLD Server")
    if not auth_server:
        return f"TLD Server không phản hồi hoặc không có {second_level} (t= {time.time() - t2:.4f}s)"
    print(f"TLD → Authoritative: {auth_server} (t= {time.time() - t2:.4f}s)")

    # Truy vấn Authoritative Server
    t3 = time.time()
    auth_data = auth_servers.get(auth_server, {})
    ip = safe_lookup(auth_data, domain, label="Authoritative Server")
    if not ip:
        return f" Authoritative Server không phản hồi hoặc không có IP cho {domain} (t= {time.time() - t3:.4f}s)"
    print(f" Authoritative → IP: {ip} (t= {time.time() - t3:.4f}s)")

    # Tổng thời gian
    print(f"Tổng thời gian: {time.time() - start:.4f}s")
    return ip

# Gọi thử các truy vấn
if __name__ == "__main__":
    print(resolve("www.example.com"))
    print("-" * 40)
    print(resolve("mail.example.com"))
    print("-" * 40)
    print(resolve("shop.myorg.org"))
    print("-" * 40)
    print(resolve("unknown.example.com"))  # không có IP
    print("-" * 40)
    print(resolve("invalid"))  # tên miền không hợp lệ
