

from sys import stdin
import array
stdin.readline()

d = map(long, stdin.read(-1).split())
a = array.array('L')
b = array.array('L')
a.fromlist(d[0::2])
b.fromlist(d[1::2])
c = array.array('L')
c.fromlist([x*y for x, y in zip(a, b)])
print a * b


