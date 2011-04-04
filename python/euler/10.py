
import math


T = 3000000




t = range(T)


for v in range(2, int(math.sqrt(T))):
    if t[v] is None:
        continue

    for x in range(v*2, T, v):
        t[x] = None



primes = filter(None, t)

assert primes.pop(0) == 1
assert primes[0] == 2
#print primes
print sum([x for x in primes if x < 2000000])


