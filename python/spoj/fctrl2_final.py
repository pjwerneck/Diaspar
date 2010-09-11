from sys import stdin
from operator import mul
stdin.readline()


c = [1, 1] + [reduce(mul, xrange(2, x+1)) for x in xrange(2, 24)]
c.extend([c[-1]*reduce(mul, xrange(24, x+1)) for x in range(24, 48)])
c.extend([c[-1]*reduce(mul, xrange(48, x+1)) for x in range(48, 71)])

def fac(n):
    if n < 70:
        return c[n]
    else:
        return n*fac(n-1)
    
print '\n'.join(map(str, map(fac, map(int, stdin.read(-1).split()))))






def f(n):
    if n <= 1:
        return 1
    else:
        return f(n-1) * n

d = map(fac, map(int, stdin.read(-1).split()))
print len(d)
print d
for x in range(101):
    print x
    assert f(x) == fac(x)
