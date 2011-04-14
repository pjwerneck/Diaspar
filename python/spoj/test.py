
from sys import stdin
d = stdin.read()
print d[:d.index('\n42\n')]
