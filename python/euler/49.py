
import math


from sys import stdin
from random import randint

import itertools

CACHE_BIN = {}

def bin(n):
    if n in CACHE_BIN:
        return CACHE_BIN[n]

    r = []
    while (n > 0):
        r.append(n % 2)
        n = n / 2

    CACHE_BIN[n] = r
    return r


CACHE_TEST = {}

def test(a, n):
    if (a, n) in CACHE_TEST:
        return CACHE_TEST[(a, n)]
    
    b = bin(n - 1)
    d = 1
    for i in xrange(len(b)-1, -1, -1):
        x = d
        d = (d * d) % n
    
        if d == 1 and x != 1 and x != n - 1:
            CACHE_TEST[(a, n)] = 1
            return 1
  
        if b[i] == 1:
            d = (d * a) % n

    t = d != 1
    CACHE_TEST[(a, n)] = t
    return t


CACHE_MR = {1:0, 2:1}

def mr(n):
    if n in CACHE_MR:
        return CACHE_MR[n]
    
    if n % 2 == 0:
        return 0
      
    for j in xrange(100):
        if test(randint(1, n-1), n):
            CACHE_MR[n] = 0
            return 0

    CACHE_MR[n] = 1
    return 1



def check():
    primes = []

    for x in range(1000, 10000):
        if mr(x):
            primes.append(x)

    for group in itertools.combinations(primes, 3):
        a, b, c = group

        if not (set(str(a)) == set(str(b)) == set(str(c))):
            continue

        ns = [a, b, c]
        ns.sort()

        if ns[2] - ns[1] == ns[1] - ns[0]:
            print ns

        
    

check()
