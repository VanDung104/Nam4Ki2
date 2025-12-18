import multiprocessing
import concurrent.futures
import time
import math
from functools import partial

def split_list(numbers, num_workers):
    """Chia danh sách thành các phần bằng nhau"""
    chunk_size = len(numbers) // num_workers
    return [numbers[i*chunk_size : (i+1)*chunk_size] for i in range(num_workers)]

def sum_partial(numbers):
    """Tính tổng một phần danh sách"""
    return sum(numbers)

def is_prime(n):
    """Kiểm tra số nguyên tố"""
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def sum_primes(numbers):
    """Tính tổng các số nguyên tố trong danh sách"""
    return sum(n for n in numbers if is_prime(n))

def benchmark(func, *args):
    """Đo thời gian thực thi"""
    start = time.time()
    result = func(*args)
    end = time.time()
    return result, end - start

def run_tests(numbers, num_processes, num_threads):
    """Chạy các bài kiểm tra hiệu năng"""
    
    # Test 1: Tính tổng đơn luồng
    single_result, single_time = benchmark(sum, numbers)
    print(f"\nSingle-thread sum: {single_result}")
    print(f"Time: {single_time:.4f}s")

    # Test 2: Tính tổng đa tiến trình
    chunks = split_list(numbers, num_processes)
    with multiprocessing.Pool(num_processes) as pool:
        mp_result, mp_time = benchmark(pool.map, sum_partial, chunks)
    print(f"\nMulti-process sum ({num_processes} processes): {sum(mp_result)}")
    print(f"Time: {mp_time:.4f}s")
    print(f"Speedup: {single_time/mp_time:.2f}x")

    # Test 3: Tính tổng đa luồng
    chunks = split_list(numbers, num_threads)
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        mt_result, mt_time = benchmark(executor.map, sum_partial, chunks)
    print(f"\nMulti-thread sum ({num_threads} threads): {sum(mt_result)}")
    print(f"Time: {mt_time:.4f}s")
    print(f"Speedup: {single_time/mt_time:.2f}x")

    # Test 4: Tính tổng số nguyên tố đa tiến trình
    prime_numbers = list(range(1, 10**5))
    chunks = split_list(prime_numbers, num_processes)
    with multiprocessing.Pool(num_processes) as pool:
        prime_result, prime_time = benchmark(pool.map, sum_primes, chunks)
    print(f"\nPrime sum ({num_processes} processes): {sum(prime_result)}")
    print(f"Time: {prime_time:.4f}s")

if __name__ == "__main__":
    # Cấu hình
    NUMBERS = list(range(1, 10**7 + 1))  # Tăng lên 10 triệu số
    NUM_PROCESSES = 4
    NUM_THREADS = 4

    print("=== Benchmarking Parallel Computing ===")
    print(f"Data size: {len(NUMBERS):,} elements")
    print(f"Processes: {NUM_PROCESSES}, Threads: {NUM_THREADS}")

    run_tests(NUMBERS, NUM_PROCESSES, NUM_THREADS)
