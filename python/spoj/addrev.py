
from sys import stdin


d = [s.split() for s in stdin.readlines()[1:]]

d = map(int, stdin.read(-1)[::-1].split())

d = map(lambda s: str(s).rstrip('0'), map(sum, zip(d[0::2], d[1::2])))

s = '\n'.join(d)[::-1]
print s
