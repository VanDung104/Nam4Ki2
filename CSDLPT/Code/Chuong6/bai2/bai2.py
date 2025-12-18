import time
from collections import OrderedDict

class DNSCache:
    def __init__(self, capacity=5):
        self.cache = OrderedDict()
        self.capacity = capacity
        self.hits = 0
        self.misses = 0

    def get(self, domain):
        now = time.time()
        if domain in self.cache:
            ip, expiry = self.cache[domain]
            if now < expiry:
                self.cache.move_to_end(domain)  # LRU update
                self.hits += 1
                print(f"[Cache HIT] {domain} -> {ip}")
                return ip
            else:
                print(f"[Cache EXPIRED] {domain}")
                del self.cache[domain]
        self.misses += 1
        print(f"[Cache MISS] {domain}")
        return None

    def set(self, domain, ip, ttl):
        if domain in self.cache:
            del self.cache[domain]
        elif len(self.cache) >= self.capacity:
            evicted = self.cache.popitem(last=False)  # LRU eviction
            print(f"[Cache EVICTED] {evicted[0]}")
        expiry = time.time() + ttl
        self.cache[domain] = (ip, expiry)
        print(f"[Cache SET] {domain} -> {ip} (TTL {ttl}s)")

    def flush(self):
        self.cache.clear()
        print("[Cache FLUSHED]")

    def stats(self):
        return self.hits, self.misses


class DNSServer:
    def __init__(self):
        self.records = {
            "www.example.com": "192.0.2.1",
            "mail.example.com": "192.0.2.2",
            "shop.example.com": "192.0.2.3",
            "www.myorg.org": "198.51.100.1",
            "mail.myorg.org": "198.51.100.2"
        }

    def resolve(self, domain):
        time.sleep(0.2)  # Giả lập độ trễ
        ip = self.records.get(domain)
        if ip:
            print(f"[DNS Query] Resolved {domain} -> {ip}")
            return ip
        else:
            print(f"[DNS Query] {domain} not found")
            return None


def main():
    dns_server = DNSServer()
    cache = DNSCache(capacity=3)

    while True:
        print("\n=== DNS Cache Simulator ===")
        print("1. Resolve domain")
        print("2. Flush cache")
        print("3. View cache stats")
        print("4. Exit")
        choice = input("Select option: ")

        if choice == "1":
            domain = input("Enter domain: ").strip()
            ttl = int(input("Enter TTL (s): "))
            ip = cache.get(domain)
            if ip is None:
                ip = dns_server.resolve(domain)
                if ip:
                    cache.set(domain, ip, ttl)
        elif choice == "2":
            cache.flush()
        elif choice == "3":
            hits, misses = cache.stats()
            print(f"[Stats] Cache Hits: {hits}, Misses: {misses}")
        elif choice == "4":
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
