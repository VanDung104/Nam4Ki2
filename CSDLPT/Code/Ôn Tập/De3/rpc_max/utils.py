import time

def is_prime(n):
    if n <= 1: return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0: return False
    return True

def get_primes(numbers):
    return [n for n in numbers if is_prime(n)]
