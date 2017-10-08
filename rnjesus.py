"""
This module contains number generators.
"""
from helper import *


def congruential(x, m, a, c):
    # check valid params...
    assert m >= 2, "m should be greater than 1"
    assert a < m, "a should be less than m"
    assert a >= 0, "a shouldn't be negative"
    assert c < m, "c should be less than m"
    assert c >= 0, "c shouldn't be negative"
    assert x < m, "x should be less than m"

    while 1:
        yield x
        x = (a*x + c) % m


def quad_congruential(x, m, d, a, c):
    # check params...
    assert m >= 2, "m should be greater than 1"
    assert a < m, "a should be less than m"
    assert a >= 0, "a shouldn't be negative"
    assert c < m, "c should be less than m"
    assert c >= 0, "c shouldn't be negative"
    assert x < m, "x should be less than m"

    while 1:
        yield x
        x = (d * x**2 + a*x + c) % m


def fibonachi(m):
    x1, x2 = 0, 1
    while 1:
        yield (x2 - x1) % m
        x1, x2 = x2, x1+x2


def reverse_congruential(x, p, a, c):
    assert is_prime(p)
    assert a < p
    assert a < c
    while 1:
        yield x
        rx = get_reversed(x, p)
        if rx != -1:
            raise StopIteration
        x = (a*rx + c) % p


def union(method1, method2, m):
    while 1:
        try:
            yield (next(method1) - next(method2)) % m
        except Exception as error:
            print(error)
            raise StopIteration


def get(method, start, end):
    """Return list of values generator by given method"""
    return [next(method) for i in range(end) if i >= start]


class Generator(object):
    """Generate pseudo-random number"""

    def __init__(self, method, p):
        self.method = method
        self.p = float(p)

    def next(self):
        """Return number from 0 to 1"""
        return next(self.method) / self.p

    def range(self, s, e):
        """Return number in given range"""
        return int(s + self.next() * (e - s))


if __name__ == "__main__":
    print("Congruential check:")
    c = congruential(666, get_prime(2**32), get_prime(2**16), get_prime(2**4))
    print("Result: ", get(c, 0, 20))

    d = get_prime(2**20)
    a = get_prime(d-1)
    c = get_prime(a-1)
    m = get_prime(get_prime(2**32)-1)
    result = get(quad_congruential(d, m, d, a, c), 0, 20)
    print("Sqare congruential check\nResult: ", result, "\n")
    print("Let's check collision... result size: {} and set size: {}\n".format(len(result), len(set(result))))
    print("Generator test")
    g = Generator(quad_congruential(d, m, d, a, c), m)
    for i in range(50):
        print("I:{}\nNext: {}\nRange: {}".format(i, g.next(), g.range(i, i+10)))


