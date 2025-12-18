import random
import time
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class DNSServer:
    name: str
    is_active: bool = True
    failure_rate: float = 0.0
    response_delay: float = 0.0

class DNSResolver:
    def __init__(self):
        self.servers = [
            DNSServer("dns_primary", failure_rate=0.3),
            DNSServer("dns_secondary_1"),
            DNSServer("dns_secondary_2")
        ]
        self.stats = {
            'total_queries': 0,
            'primary_failures': 0,
            'fallbacks': 0,
            'success': 0,
            'failures': 0
        }
    
    def simulate_dns_query(self, server: DNSServer, domain: str) -> Optional[str]:
        """Mô phỏng truy vấn DNS đến một server"""
        if not server.is_active:
            return None
        
        # Mô phỏng độ trễ phản hồi
        if server.response_delay > 0:
            time.sleep(server.response_delay)
        
        # Mô phỏng tỷ lệ thất bại
        if random.random() < server.failure_rate:
            return None
        
        # Tạo IP giả lập từ tên miền
        ip_parts = []
        for part in domain.split('.'):
            ip_parts.append(str(sum(ord(c) for c in part) % 256))
        return f"192.168.{ip_parts[0]}.{ip_parts[1]}"
    
    def resolve(self, domain: str, timeout: float = 1.0) -> str:
        """Phân giải tên miền với cơ chế failover"""
        self.stats['total_queries'] += 1
        result = None
        
        for i, server in enumerate(self.servers):
            try:
                start_time = time.time()
                result = self.simulate_dns_query(server, domain)
                
                if result is not None:
                    if i > 0:  # Nếu dùng backup server
                        self.stats['fallbacks'] += 1
                        print(f"[FALLBACK] Using {server.name} for {domain}")
                    
                    self.stats['success'] += 1
                    return result
                else:
                    if i == 0:
                        self.stats['primary_failures'] += 1
                    print(f"[ERROR] {server.name} failed for {domain}")
            
            except Exception as e:
                print(f"[EXCEPTION] Error querying {server.name}: {str(e)}")
        
        self.stats['failures'] += 1
        return f"[ERROR] Failed to resolve {domain} after trying all servers"
    
    def toggle_server(self, server_name: str, active: bool):
        """Bật/tắt máy chủ DNS"""
        for server in self.servers:
            if server.name == server_name:
                server.is_active = active
                print(f"Server {server_name} is now {'active' if active else 'inactive'}")
                return
        print(f"Server {server_name} not found")
    
    def set_server_properties(self, server_name: str, failure_rate: float = None, delay: float = None):
        """Thiết lập thuộc tính máy chủ"""
        for server in self.servers:
            if server.name == server_name:
                if failure_rate is not None:
                    server.failure_rate = failure_rate
                if delay is not None:
                    server.response_delay = delay
                print(f"Updated {server_name} properties")
                return
        print(f"Server {server_name} not found")
    
    def get_stats(self):
        """Lấy thống kê hoạt động"""
        stats = self.stats.copy()
        stats['primary_failure_rate'] = (
            stats['primary_failures'] / stats['total_queries'] 
            if stats['total_queries'] > 0 else 0
        )
        return stats

def main():
    resolver = DNSResolver()
    
    while True:
        print("\n=== DNS RESOLVER SIMULATOR ===")
        print("1. Resolve domain")
        print("2. Toggle server status")
        print("3. Set server properties")
        print("4. View statistics")
        print("5. Exit")
        
        choice = input("Select option: ")
        
        if choice == '1':
            domain = input("Enter domain to resolve: ")
            result = resolver.resolve(domain)
            print(f"Result: {result}")
        
        elif choice == '2':
            server = input("Enter server name: ")
            status = input("Activate (1) or deactivate (0): ")
            resolver.toggle_server(server, status == '1')
        
        elif choice == '3':
            server = input("Enter server name: ")
            try:
                failure_rate = float(input("New failure rate (0-1): "))
                delay = float(input("Response delay (seconds): "))
                resolver.set_server_properties(server, failure_rate, delay)
            except ValueError:
                print("Invalid input")
        
        elif choice == '4':
            stats = resolver.get_stats()
            print("\n=== STATISTICS ===")
            print(f"Total queries: {stats['total_queries']}")
            print(f"Primary failures: {stats['primary_failures']}")
            print(f"Primary failure rate: {stats['primary_failure_rate']:.2%}")
            print(f"Fallbacks to secondary: {stats['fallbacks']}")
            print(f"Successful resolutions: {stats['success']}")
            print(f"Failed resolutions: {stats['failures']}")
        
        elif choice == '5':
            print("Exiting...")
            break
        
        else:
            print("Invalid option")

if __name__ == "__main__":
    main()