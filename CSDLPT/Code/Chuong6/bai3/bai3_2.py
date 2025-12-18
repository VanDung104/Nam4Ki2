import random
import time

# Danh sách máy chủ DNS với dữ liệu, trạng thái và timeout
dns_servers = {
    "dns_primary": {
        "active": True,
        "data": {
            "example.com": "93.184.216.34",
            "openai.com": "104.18.7.218"
        },
        "timeout": 1
    },
    "dns_secondary": {
        "active": True,
        "data": {
            "example.com": "93.184.216.34"
        },
        "timeout": 1.5
    },
    "dns_backup_1": {
        "active": True,
        "data": {
            "openai.com": "104.18.7.218"
        },
        "timeout": 2
    }
}

# Thống kê hoạt động
stats = {
    "primary_failures": 0,
    "fallback_count": 0
}

# Xác suất lỗi máy chủ chính
primary_failure_chance = 0.3


#HÀM PHÂN GIẢI TÊN MIỀN

def resolve(domain):
    print(f"\nĐang phân giải: {domain}")

    for name, server in dns_servers.items():
        if not server["active"]:
            print(f" [{name}] Máy chủ đang TẮT.")
            continue

        # Mô phỏng lỗi máy chủ chính
        if name == "dns_primary" and random.random() < primary_failure_chance:
            print(f"[{name}] Máy chủ CHÍNH gặp lỗi (mô phỏng).")
            stats["primary_failures"] += 1
            continue

        print(f" [{name}] Đang truy vấn...")
        time.sleep(server["timeout"])  # Mô phỏng độ trễ

        ip = server["data"].get(domain)
        if ip:
            if name != "dns_primary":
                stats["fallback_count"] += 1
            print(f"[{name}] Phân giải thành công: {domain} → {ip}")
            return ip
        else:
            print(f"[{name}] Không tìm thấy tên miền.")

    print("Không phân giải được tên miền sau khi thử tất cả máy chủ.")
    return None

# BẬT/TẮT MÁY CHỦ DNS

def toggle_server(server_name, status):
    if server_name in dns_servers:
        dns_servers[server_name]["active"] = status
        print(f"Máy chủ '{server_name}' đã được {'BẬT' if status else 'TẮT'}.")
    else:
        print(f"Máy chủ '{server_name}' không tồn tại.")


# ==============================
# THIẾT LẬP TIMEOUT
# ==============================
def set_timeout(server_name, timeout_value):
    if server_name in dns_servers:
        dns_servers[server_name]["timeout"] = timeout_value
        print(f"Timeout của '{server_name}' được đặt là {timeout_value} giây.")
    else:
        print(f"Không tồn tại máy chủ '{server_name}'.")


# ==============================
#  HIỂN THỊ THỐNG KÊ
# ==============================
def print_stats():
    print("\nTHỐNG KÊ HỆ THỐNG:")
    print(f"- Số lần máy chủ chính gặp lỗi: {stats['primary_failures']}")
    print(f"- Số lần fallback sang máy chủ phụ: {stats['fallback_count']}")


# ==============================
# ➕ THÊM MÁY CHỦ MỚI
# ==============================
def add_dns_server(name, data, timeout=1.5):
    if name in dns_servers:
        print(f"Máy chủ '{name}' đã tồn tại.")
        return
    dns_servers[name] = {
        "active": True,
        "data": data,
        "timeout": timeout
    }
    print(f"Đã thêm máy chủ mới: {name}")



if __name__ == "__main__":
    resolve("example.com")
    resolve("openai.com")
    resolve("nonexistent.com")

    toggle_server("dns_primary", False)  # Tắt máy chủ chính
    resolve("example.com")
    toggle_server("dns_primary", True)   # Bật lại

    set_timeout("dns_secondary", 3)  # Thay đổi timeout máy phụ

    add_dns_server("dns_backup_2", {"newsite.com": "1.2.3.4"}, timeout=2)
    resolve("newsite.com")

    print_stats()
