from multiprocessing import cpu_count, Pool
from time import time


def single_number_factorize(number):
    result = []
    for i in range(1, number + 1):
        if number % i == 0:
            result.append(i)
    return result


def factorize(*numbers):
    results = []
    for number in numbers:
        results.append(single_number_factorize(number))
    return results


def multi_process_factorize(*numbers):
    with Pool(cpu_count()) as pool:
        results = pool.map(single_number_factorize, numbers)
    return results


if __name__ == "__main__":
    factorize_time_start = time()
    a, b, c, d = factorize(128, 255, 99999, 10651060)
    factorize_time_end = time()

    multi_process_factorize_time_start = time()
    a, b, c, d = multi_process_factorize(128, 255, 99999, 10651060)
    multi_process_factorize_time_end = time()

    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]

    print(f"Single proccess factorize time: {factorize_time_end-factorize_time_start}")
    print(f"Multi proccess factorize time: {multi_process_factorize_time_end-multi_process_factorize_time_start}")
