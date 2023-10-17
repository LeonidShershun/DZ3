import time
from multiprocessing import Pool, cpu_count


def factorize_intro(num):
    factors = []
    for i in range(1, num + 1):
        if num % i == 0:
            factors.append(i)
    return factors


def factorize(*numbers):
    return [factorize_intro(n) for n in numbers]


def factorize_paralleles(*numbers):
    with Pool(cpu_count()) as p:
        return p.map(factorize_intro, numbers)


if __name__ == "__main__":
    start = time.time()
    a, b, c, d = factorize(128, 255, 99999, 10651060)
    end = time.time()
    print(f"\nSynchron execution time: {end - start} seconds.")

    start = time.time()
    a, b, c, d = factorize_paralleles(128, 255, 99999, 10651060)
    end = time.time()
    print(f"\nParallel execution time: {end - start} seconds.\n")
    print('assert a =', a)
    print('assert b =', b)
    print('assert c =', c)
    print('assert d =', d, "\n")
