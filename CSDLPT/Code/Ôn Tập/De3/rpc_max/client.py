import requests, threading, time
from concurrent.futures import ThreadPoolExecutor

NAME_SERVER = 'http://localhost:5000'
SERVICE_NAME = 'prime_service'

jobs = list(range(1, 1000))
server_stats = {}
lock = threading.Lock()
results = []

def fetch_servers():
    return requests.get(f'{NAME_SERVER}/resolve/{SERVICE_NAME}').json()

def task(server, chunk):
    start = time.time()
    try:
        res = requests.post(f'{server}/primes', json={'numbers': chunk}, timeout=3)
        primes = res.json()
    except:
        return False, chunk, None, 0
    duration = time.time() - start
    with lock:
        server_stats.setdefault(server, {'count': 0, 'time': 0})
        server_stats[server]['count'] += 1
        server_stats[server]['time'] += duration
        results.extend(primes)
    return True, chunk, server, duration

if __name__ == '__main__':
    all_start = time.time()
    servers = fetch_servers()
    chunks = [jobs[i::len(servers)] for i in range(len(servers))]

    with ThreadPoolExecutor(max_workers=len(servers)) as executor:
        futures = []
        for server, chunk in zip(servers, chunks):
            futures.append(executor.submit(task, server, chunk))

        for future in futures:
            success, chunk, server, dur = future.result()
            if not success:
                for s in servers:
                    if s != server:
                        task(s, chunk)
                        break

    total_time = time.time() - all_start
    print(f'Total time: {total_time:.2f}s')
    print(f'All primes found: {sorted(results)}')
    for server, stat in server_stats.items():
        avg_time = stat['time'] / stat['count']
        print(f"Server {server}: handled {stat['count']} chunks, avg response {avg_time:.2f}s")
