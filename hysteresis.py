#-*- coding: utf-8 -*-
"""This module contains hysteresis matrix mathod calculation.
"""
from math import factorial as fact


def get_default_settings():
    settings = {}
    settings['h1'] = 1
    settings['h2'] = 2
    settings['mu'] = 3
    settings['v'] = 4
    settings['c1'] = 5
    settings['c2'] = 5
    settings['c3'] = 5
    settings['c4'] = 5
    settings['c5'] = 5
    settings['n'] = 3
    settings['c'] = 6
    settings['v'] = 5
    return settings

def P(g):
    """Shortcut for П"""
    mult = 1
    for i in g:
        mult *= i
    return mult


def inf_sum(i, func, accuracy=0.00001, step=1):
    res, a = 0, func(i)
    b = a + accuracy * 2
    while abs(b-a) > accuracy:
        res, i = res+a, i+1
        a, b = func(i), a
    return res


def calculate(H1, H2, p=None):
    if not p:
        p = get_default_settings()

    h = (0, p['h1'], p['h2'])
    h1, h2 = h[1], h[2]
    mu = p['mu']

    N = p['n']
    c = p['c']

    C1 = p['c1']
    C2 = p['c2']
    C3 = p['c3']
    C4 = p['c4']
    C5 = p['c5']
    v = p['v']

    end = 100

    def get_base_p(r, j, to):
        """Return shared part for alpha and beta functions"""
        return P((h[r] + v*(j-k)) / (h[r] + mu + v*(j-k)) for k in range(to))

    def base_p_generator(r, j, to):
        i, result = 0, 1
        while i < to:
            result *= get_base_p(r, j, i)
            i += 1
            yield result

    def get_a(r, j):
        """Return alpha element"""
        return (h[r]**j / (fact(j)*(v**j)) * get_base_p(r, j, j))

    def get_b(r, j, m):
        """Return beta element"""
        fj = fact(j)
        gen_base = base_p_generator(r, j, j-m+1)
        return sum(fact(j-i-1)*(h[r]**i)*next(gen_base) / (fj*(v**i)) for i in range(j-m+1))

    def get_p10(H1, H2):
        return 1 / (((mu + h1) / h1)
            + sum(get_a(1, j) * (h1 + mu + j*v) / (h1 + j*v) for j in range(1, H1+1))
            + sum((h1 + mu + j*v) / (h1 + j*v) * (get_a(1, j) - (h1*get_a(1, H2)*get_b(1, j, H1+1))) for j in range(H1+1, H2+1))
            + ((h1*get_a(1, H2)) / (v + h1*get_b(1, H2, H1+1)))*(1/(H1+1) + sum((get_b(2, j, H1+1)*(h2+mu+j*v)) / (h2 + j*v) for j in range(H1+2, H2+1+1))
            + inf_sum(H2+2, lambda j: ((h2 + mu + j*v)*get_a(2, j)*get_b(2, H2+1, H1+1) / (get_a(2, H2+1)*(h2 + j*v))))))

    H = 100
    p1 = [[0 for _ in range(H2+1)] for _ in range(2)]
    p2 = [[0 for _ in range(H1, end+1)] for _ in range(2)]


    p1[1][0] = get_p10(H1, H2)
    p1[0][0] = (mu / h1)*p1[1][0]
    for j in range(1, H1+1):
        a = get_a(1, j)
        p1[0][j] = (mu*a*p1[1][0]) / (h1 + j*v)
        p1[1][j] = a*p1[1][0]

    for j in range(H1+1, H2+1):
        a = get_a(1,j)
        p1[1][j] = (a - (h1*get_a(1, H2)*get_b(1, j, H1+1)) / (v+h1*get_b(H2, H1+1)))*p1[1][0]
        p1[0][j] = (mu / (h1 + j*v))*p1[1][j]

    p2_h1p1_shared = (get_a(1, H2)*h1*p1[1][0]) / ((H1+1)*(mu + h2 + (H1+1)*v)*(v + h1*get_b(1, H2, H1+1)))
    p2[0][H1+1] = mu * p2_h1p1_shared
    p2[1][H1+1] = (h2 + (H1+1)*v) * p2_h1p1_shared

    for j in range(H1+2, H2+2):
        p2[1][j] = (h1*get_a(1, H2)*get_b(2, j, H1+1)) / (v + h1*get_b(1, H2, H1+1))
        p2[0][j] = (mu / (h2 + j*v)) * p2[1][j]

    for j in range(H2+2, end+1):
        p2[1][j] = p1[1][0] * (get_a(2, j)*h1*get_a(1, H1)*get_b(2, H2+1, H1+1)) / (get_a(2, H2+1)*(v + h1*get_b(1, H2, H1+1)))
        p2[0][j] = p2[1][j] * (mu / (h2 + j*v))

    def L1(H1, H2):
        return mu * sum(p1[1][j] for j in range(H2+1))

    def L2(H1, H2):
        return mu * inf_sum(H1+1, lambda j: p2[1][j])

    def L3(H1, H2):
        return h1*sum(p1[1][j] for j in range(H2+1)) + h2*inf_sum(H1+1, lambda j: p2[1][j])

    def L4(H1, H2):
        return h1*p1[c][H2] + (H1+1)*v*(p2[0][H1+1] + p2[1][H1+1])

    def L5(H1, H2):
        return v*(sum(j*p1[1][j] for j in range(1, H2+1)) + inf_sum(H1+1, lambda j: j*p2[1][j]))

    def L(H1, H2):
        return C1*L1(H1, H2) + C2*L2(H1, H2) - C3*L3(H1, H2) - C4*L4(H1, H2) - C5*L5(H1, H2)
    
    return L(H1, H2)


if __name__ == "__main__":
    print("Test run")
    print("Infinite sum.")
    sum_res = inf_sum(1, lambda j: 10/j)
    end = 100
    results = [[None]*end for _ in range(end)]
    for th1 in range(end):
        for th2 in range(th1+1):
            result[th1][th2] = calculate(th1, th2)
    print(result)

