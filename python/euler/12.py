
from math import sqrt



def triangles():
    t = 0
    c = 1
    while 1:
        t += c
        c += 1
        yield t


def factors(n):
    f = []
    for v in xrange(1, int(sqrt(n))):
        if n % v == 0:
            f.append(v)
            f.append(n/v)
    return f

        
t = triangles()


for n in t:
    if n < 5000000:
        continue
    d = factors(n)
    if len(d) > 500:
        d.sort()        
        print n, len(d), d
        break
