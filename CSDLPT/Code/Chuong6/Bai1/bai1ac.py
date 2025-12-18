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

# Hàm phân giải DNS
def resolve(domain):
    print(f"Resolving: {domain}")
    start = time.time()

    # Bước 1: lấy TLD
    parts = domain.split(".")
    if len(parts) < 2:
        return "Tên miền không hợp lệ"
    tld = "." + parts[-1]

    t1 = time.time()
    tld_server = root_server.get(tld)
    if not tld_server:
        return f"Không tìm thấy TLD Server cho {tld} (t= {time.time() - t1:.4f}s)"
    print(f"Root → TLD: {tld_server} (t= {time.time() - t1:.4f}s)")

    # Bước 2: lấy domain cấp 2
    second_level = ".".join(parts[-2:])
    t2 = time.time()
    auth_server = tld_servers.get(tld_server, {}).get(second_level)
    if not auth_server:
        return f"Không tìm thấy Authoritative Server cho {second_level} (t= {time.time() - t2:.4f}s)"
    print(f"TLD → Authoritative: {auth_server} (t= {time.time() - t2:.4f}s)")

    # Bước 3: tìm IP
    t3 = time.time()
    ip = auth_servers.get(auth_server, {}).get(domain)
    if not ip:
        return f"Không tìm thấy IP cho {domain} (t= {time.time() - t3:.4f}s)"
    print(f" Authoritative → IP: {ip} (t= {time.time() - t3:.4f}s)")
    print(f"Tổng thời gian: {time.time() - start:.4f}s")
    return ip

if __name__ == "__main__":
    print(resolve("www.example.com"))
    print("-" * 40)
    print(resolve("mail.example.com"))
    print("-" * 40)
    print(resolve("shop.myorg.org"))
    print("-" * 40)
    print(resolve("unknown.example.com"))  # domain không tồn tại
    print("-" * 40)
    print(resolve("invalid"))  # tên miền không hợp lệ

