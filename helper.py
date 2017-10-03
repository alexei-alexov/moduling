"""
This module contains all helper functions used in this project.
"""

# this list contain all prime numbers. used to optimize process.
_filter = [2, 3, 5, 7, 11, 13]

def is_prime(num):
    """Return is num is prime."""
    if num <= 1:
        return False
    if num == 2:
        return True
    if not num & 1:
        return False

    for i in range(3, int(num**0.5)+1, 2):
        if not (num % i):
            return False
    return True

def get_prime(threshold):
    """Return greatest number which is less than given threshold.

    Return -1 if there is no such number.
    """
    check_num = threshold
    while check_num > 1:
        if is_prime(check_num):
            return check_num
        check_num -= 1
    return -1


INF = "infinite"
def get_reversed(x, p):
    """Return reversed number of x with p mod
    If x is zero - return infinite.
    If x is infinite - return zero.
    Return -1 if there is no such number
    """
    if not x:
        return INF
    if x == INF:
        return 0

    for n in range(2, p):
        if (n*x) % p == 1:
            return n
    return -1


if __name__ == "__main__":
    print("testing is_prime function")
    for test_case in (2, 3, 5, 6, 9, 10, 100, 11, 19, 123):
        print("checking {} :: is_prime: {}".format(test_case, is_prime(test_case)))

    threshold = 2 ** 32
    print("get_prime for {} = :: = {}".format(threshold, get_prime(threshold)))

    alph_size = 26
    for num in range(alph_size):
        print("reversed: {} -> {}".format(num, get_reversed(num, alph_size)))


