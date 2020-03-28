import random
import sets

def modular_exponential(x, y, N):
    """
        find the value for (x**y)%N
    """
    cache = {}
    return modular_exponential_impl(x, y, N, cache)

def modular_exponential_impl(x, y, N, cache):
    if y == 0:
        cache[y] = 1%N
    elif y == 1:
        cache[y] = x%N
    elif cache.get(y) is None:
        if y%2 == 1:
            cache[y] = (modular_exponential_impl(x, 1, N, cache) * \
                        modular_exponential_impl(x, y-1, N, cache))%N
        else:
            cache[y] = ((modular_exponential_impl(x, y/2, N, cache) ** 2)%N)
    return cache[y]

def euclid(x, y):
    """
        find gcd(x, y)
    """
    if x == 0 or y == 0:
        return x+y

    large, small = (x, y) if x > y else (y, x)
    return euclid(large%small, small)

def ext_euclid(x, y):
    """
        find d = gcd(x, y) and d = alpha*x + beta*y
    """
    if y == 0:
        return x, 1, 0

    d, alpha, beta = ext_euclid(y, x%y)
    return d, beta, alpha-(x/y)*beta

def get_prime(n = 8, k = 100):
    """
        get random prime number in [2,2**n)
        args:
            n = number of bit of random prime number
            k = number of fermat tests to be performed
    """
    is_prime = False
    r = None

    while not is_prime:
        is_prime = True
        r = random.randint(2, 2**n-1)
        is_visited = sets.Set()
        # perform fermat test k times for k numbers
        for i in range(k):
            z = random.randint(2, r)
            while z in is_visited:
                z = random.randint(2, r)
            is_visited.add(z)
            if modular_exponential(z, r-1, r) != 1:
                is_prime = False
                break

    return r
