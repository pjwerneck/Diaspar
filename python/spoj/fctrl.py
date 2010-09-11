from sys import stdin
from math import log, ceil
from operator import mul, div
#stdin.readline()
data = range(1, 100000)
out = open('/dev/null', 'w')



def main1():
    d = [0, 1, 6, 31, 156, 781, 3906, 19531, 97656, 488281, 2441406, 12207031, 61035156, 305175781]
    def Z(n):
        i = 1
        t = 0
        while 1:
            z = n/(5**i)
            if z > 0:
                t += z
                i += 1
            else:
                break
        
        return t

    c = map(str, map(Z, data))
    print >> out, '\n'.join(c)



