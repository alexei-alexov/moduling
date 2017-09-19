#-*- coding: utf-8 -*-
"""This module contains hysteresis matrix mathod calculation.
"""
from math import factorial as fact


def get_default_settings():
    settings = {}
    settings['h1'] = 1
    settings['h2'] = 2
    settings['mu'] = 3
    settings['nu'] = 4
    settings['c1'] = 5
    settings['c2'] = 5
    settings['c3'] = 5
    settings['c4'] = 5
    settings['c5'] = 5
    settings['n'] = 3
    settings['c'] = 6

def P(g):
    """Shortcut for П"""
    mult = 1
    for i in g:
        mult *= i
    return mult

def calculate(p=None):
    if not p:
        p = get_default_setting()

    h = (0, p['h1'], p['h2'])
    mu = p['mu']
    nu = p['nu']

    N = p['n']
    c = p['c']

    C1 = p['c1']
    C2 = p['c2']
    C3 = p['c3']
    C4 = p['c4']
    C5 = p['c5']

    def get_base_p(r, j, to):
        """Return shared part for alpha and beta functions"""
        return P((h[r] + nu*(j-k)) / (h[r] + mu + nu*(j-k)) for k in xrange(to))

    def base_p_generator(r, j, to):
        i, result = 0, 1
        while i < to:
            result *= get_base_p(r, j, i)
            i += 1
            yield result

    def get_a(r, j):
        """Return alpha element"""
        return (h[r]**j / (fact(j)*(nu**j)) * get_base_p(r, j, j)

    def get_b(r, j, m):
        """Return beta element"""
        fj = fact(j)
        gen_base = base_p_generator(r, j, j-m+1)
        return sum(fact(j-i-1)*(h[r]**i)*next(gen_base) / (fj*(nu**i)) for i in xrange(j-m+1))

