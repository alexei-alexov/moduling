from helper import get_prime
from rnjesus import (Generator, fibonachi,
        congruential, quad_congruential, reverse_congruential)


class Polygon(object):
    """This is representation of four point figure"""

    def __init__(self, p):
        self.p = p

    def is_in(self, x, y):
        """Return True is point is belong to polygon"""
        result = False
        p0x, p0y = self.p[0]
        for i in range(1, len(self.p) + 1):
            p1x, p1y = self.p[i % len(self.p)]
            # check if point in line
            try:
                if ((x - p0x) / (p0x - p1x)) == ((y - p0y) / (p0y - p1y)): return True
            except ZeroDivisionError:
                return True
            # check if line inside of polygon
            if ((p0y > y) != (p1y > y)) and (x < (p1x - p0x) * (y - p0y) / (p1y - p0y) + p0x):
                result = not result
            p0x, p0y = p1x, p1y
        return result


def calculate(random, figure, frame, m=100, debug=False):
    "Calculate area using random generator"""
    xs = frame[0]
    ys = frame[1]
    minx, maxx, miny, maxy = min(xs), max(xs), min(ys), max(ys)
    dx, dy = maxx - minx, maxy - miny


    frame_area = dx * dy
    n = 0.0
    for i in range(m):
        rx = random.next()
        ry = random.next()
        shot_x = dx * rx + minx
        shot_y = dy * ry + miny
        in_f = figure.is_in(shot_x, shot_y)
        if in_f: n += 1
        if debug:
            print("rx: {} ry: {}".format(rx, ry))
            print("x: {} y: {} is in figure? {}".format(shot_x, shot_y, in_f))

    return frame_area * (n / m)


if __name__ == "__main__":
    p = []
    for i in range(4):
        print("Point {}.".format((1+i)))
        p.append((int(input("x: ")), int(input("y: "))))

    print("Your points: ", p)

    xs = tuple(i[0] for i in p)
    ys = tuple(i[1] for i in p)

    a, b, c, d = min(xs), max(xs), min(ys), max(ys)

    # generator params...
    qd = get_prime(2**20)
    qa = get_prime(d-1)
    qc = get_prime(a-1)
    qm = get_prime(get_prime(2**32)-1)

    square = ((a,c), (b,c), (a,d), (b,d))
    print("SQUARE: {}".format(square))
    methods = (
        (Generator(congruential(1, qm, qa, qa), qm), "Congruential method"),
        (Generator(quad_congruential(1, qm, qd, qa, qc), qm), "Quad congruential method"),
        (Generator(fibonachi(qm), qm), "Fibonachi method"),
#        (Generator(reverse_congruential(1, qm, qc, qa), qm), "Reverse congruential method"),
    )
    m = int(input("Enter amount of points: "))
    tries = int(input("Enter amount of tries: "))
    results = [[] for _ in range(len(methods))]
    for tries in range(tries):
        for num, (method, name) in enumerate(methods):
            results[num].append(calculate(method, Polygon(p), (xs, ys), m))

    for num, (method, name) in enumerate(methods):
        print("{}. Area: {}".format(name, sum(results[num]) / tries))

