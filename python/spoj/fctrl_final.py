#import psyco
from sys import stdin
stdin.readline()
from math import log

def _run():
    p = [5**i for i in range(1, 14)]
    for v in stdin.read().split():
        n = int(v)
        t = 0
        for x in p:
            if x > n:
                break
            t += n/x
        print t

def run():
    for v in stdin.read().split():
        n = int(v)
        print sum(n/5**i for i in range(1, int(log(n, 5))+1))

#psyco.bind(run, rec=1)

#run()
#from types import CodeType, FunctionType

#code = CodeType(0, 7, 7, 67, 'g\x00\x00\x04}\x00\x00t\x00\x00d\x01\x00d\x02\x00\x83\x02\x00D]\x11\x00}\x01\x00|\x00\x00d\x03\x00|\x01\x00\x13\x12q\x14\x00~\x00\x00}\x02\x00xb\x00t\x01\x00i\x02\x00\x83\x00\x00i\x03\x00\x83\x00\x00D]N\x00}\x03\x00t\x04\x00|\x03\x00\x83\x01\x00}\x04\x00d\x04\x00}\x05\x00x.\x00|\x02\x00D]&\x00}\x06\x00|\x06\x00|\x04\x00j\x04\x00o\x05\x00\x01Pn\x01\x00\x01|\x05\x00|\x04\x00|\x06\x00\x157}\x05\x00q`\x00W|\x05\x00GHqA\x00Wd\x00\x00S', (None, 1, 14, 5, 0), ('range', 'stdin', 'read', 'split', 'int'), ('_[1]', 'i', 'p', 'v', 'n', 't', 'x'), '', 'run', 5, '', (), ())

#run = FunctionType(code, globals())
run()


#def run():
#    p = [5**i for i in range(1, 15)]
#    for v in stdin.read().split():
#        n = int(v)
#        t = 0
#        for x in p:
#            if x > n:
#                break
#            t += n/x
#        print t




#def Z(n):
#    t = 0
#    for i in xrange(1, 14):
#        z = n/(5**i)
#        if z > 0:
#            t += z
#        else:
#            break
#    return t

#for v in map(str, map(Z, map(int, stdin.read().split()))):
#    print v


#import dis
#dis.dis(Z)
#print '-'*50
#dis.dis(run)
