

from sys import stdin

d = stdin.read()[::-1].split()
d = map(int, d)
d = map(int.__add__, d[0:-1:2], d[1::2])

d = [repr(s).rstrip('0') for s in d]

d = '\n'.join(d)[::-1]

print d





