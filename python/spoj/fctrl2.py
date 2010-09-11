from sys import stdin
from operator import mul
#stdin.readline()

read = '\n'.join(map(str, range(100)))

out = open('/dev/null', 'w')

def main1():
    c = [1, 1] + [reduce(mul, xrange(2, x+1)) for x in xrange(2, 25)]
    c.extend([c[-1]*reduce(mul, xrange(25, x+1)) for x in range(25, 50)])
    c.extend([c[-1]*reduce(mul, xrange(50, x+1)) for x in range(50, 75)])
    c.extend([c[-1]*reduce(mul, xrange(75, x+1)) for x in range(75, 101)])
    for v in map(int, read.split()):
        print >> out, c[v]

def main2():
    c = [1, 1] + [reduce(mul, xrange(2, x+1)) for x in xrange(2, 25)]
    c.extend([c[-1]*reduce(mul, xrange(25, x+1)) for x in xrange(25, 50)])
    c.extend([c[-1]*reduce(mul, xrange(50, x+1)) for x in xrange(50, 71)])

    def fac(n):
        if n < 70:
            return c[n]
        else:
            return n*fac(n-1)

    print >> out, '\n'.join(map(str, map(fac, map(int, read.split()))))
#        print >> out, v
