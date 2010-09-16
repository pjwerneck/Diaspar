

from Tkinter import *
import math
import random


def color():
    return '#' + hex(random.randint(0, 0xfff))[2:].zfill(3)
    
root = Tk()

w = h = 1000

c = Canvas(width=w, height=h, bg='white')
c.pack(expand=1, fill=BOTH)


ox, oy = w/2, h/2

a = math.radians(270)
f = math.radians(60)
s = h/6

n = []

for v in (30, 150, 270):
    va = math.radians(v+180)

    X = ox + s*math.cos(va)
    Y = oy + s*math.sin(va)
    c.create_line(ox, oy, X, Y, fill=color())
    n.append((va, X, Y))



def d(root):
    global s
    v = []
    s = s * 0.618
    for a, x, y in n:
        for i in (f, -f):
            A = a+i
            X = x + s*math.cos(A)
            Y = y + s*math.sin(A)
            v.append((A, X, Y))
            c.create_line(x, y, X, Y, fill=color())
    n[:] = v

    if len(n) < 2 ** 15:
        root.after(100, d, root)


d(root)
root.mainloop()
