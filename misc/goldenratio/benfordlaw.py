

from __future__ import division

import random
import math


def filedata1():
    rawdata = open('benfdata')

    data = []


    for line in rawdata:
        if len(line) < 40:
            continue
        if line.startswith('.'):
            continue
        line = line.split()
        try:
            s = line[4]
        except IndexError:
            print line
            raise
        data.append(s)

    return data


def filedata2():
    rawdata = open('orkut')
    data = []
    for line in rawdata:
        v = ''.join(line.split()[-1].split(','))
        data.append(v)
    return data


def filedata3():
    rawdata = open('suicide')
    data = []
    for line in rawdata:
        v = ''.join(line.split()[-2].split(','))
        v = ''.join(v.split('.'))
        data.append(v)
    return data

def filedata4():
    rawdata = open('power')
    data = []
    for line in rawdata:
        v = ''.join(line.split()[-1].split(','))
        data.append(v)
    return data


def randdata():
    data = [str(random.random())[2:] for x in range(10000)]
    return data

def realrandom():
    rawdata = open('random')
    data = [line.strip() for line in rawdata]
    return data
    

def benf(data):
    count = [0]*10

    
    for x in data:
        x = x.lstrip('0')
        if not x.strip():
            continue
        count[int(x[0])] += 1

    s = sum(count)

    for i, x in enumerate(count[1:]):
        real = math.log10(1 + 1/(i+1))*100
        v = x/s*100
        
        print '%s\t%s\t %0.2f%%\t(%0.2f%%)'%(i+1, x, v, v-real)


def fib(n):
    d = [1, 1]
    while len(d) < n:
        d.append(d[-1]+d[-2])

    d = map(str, d)
    return d
    

def pow2(n):
    d = []
    for x in range(n):
        d.append(str(3 **x))
    return d



def primes():
    rawdata = open('primes')
    data = []
    for line in rawdata:
        data.extend(line.split())
    return data


def real():
    import math
    v = [math.log10(1 + 1/d) for d in range(1, 10)]
    for i, x in enumerate(v):
        print '%s\t%0.2f%%'%(i+1, x*100)
    

benf(filedata3())
#benf(realrandom())
#benf(pow2(1000))
#benf(pow2(1000))
#benf(pow2(1000))
#benf(primes())
#real()
    
