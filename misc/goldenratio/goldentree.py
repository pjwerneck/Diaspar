

from Tkinter import *
import math

root = Tk()

w = h = 1000

c = Canvas(width=w, height=h, bg='white')
c.pack(expand=1, fill=BOTH)

ox, oy = w/2, h

a = math.radians(270)
f = math.radians(60)

c.create_line(ox, oy, ox, oy-h/2)

n = [(a, ox, oy-h/2)]

s = h/4

def d(root):
    global s
    v = []
    s = s * 0.618
    for a, x, y in n:
        for i in (-f, +f):
            A = a+i
            X = x + s*math.cos(A)
            Y = y + s*math.sin(A)
            v.append((A, X, Y))
            c.create_line(x, y, X, Y)
    n[:] = v

    if len(n) < 2 ** 15:
        root.after(100, d, root)

d(root)

root.mainloop()


