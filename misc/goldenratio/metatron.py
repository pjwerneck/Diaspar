

from __future__ import division

from Tkinter import *
from math import sin, pi, sqrt

import sys

SIDE = 800
R = SIDE/10
F = sqrt(3)/2
RF = R*F

def gratio():
    f = [1, 1, 2, 3]
    p = 0
    while 1:
        f.append(f[-1]+f[-2])
        n = (f[-2]/f[-1])
        if n == p:
            return n
        p = n
        
G = gratio()
print G
G = ((1+sqrt(5))/2)-1
        
    


class MainWindow(Tk):
    def __init__(self, *args, **kwds):
        Tk.__init__(self)

        self.canvas = Canvas(self, width=SIDE, heigh=SIDE+R, bg='white')
        self.canvas.pack()

        
        self.points = self.get_points()
        self.center = self.points[0]
        self.inner = self.points[1:7]
        self.outer = self.points[7:]

        self.golden_points = self.get_golden_points()
        
        self.build_circles()
        self.draw_lines()
        self.draw_golden_lines()

        #self.post()

    def get_points(self):
        points = []
        center = x, y = (SIDE/2, SIDE/2+R/2)

        # center circle middle
        points.append(center)

        # 6 inner circles middle
        points.append((x, y - 2*R))
        points.append((x + 2*RF, y - R))
        points.append((x + 2*RF, y + R))
        points.append((x, y + 2*R))
        points.append((x - 2*RF, y + R))
        points.append((x - 2*RF, y - R))

        # 6 outer circles middle
        points.append((x, y - 4*R))
        points.append((x + 4*RF, y - 2*R))
        points.append((x + 4*RF, y + 2*R))
        points.append((x, y + 4*R))
        points.append((x - 4*RF, y + 2*R))
        points.append((x - 4*RF, y - 2*R))
        
        return points

    def get_golden_points(self):
        points = []
        x, y = self.center

        points.append(self.outer[0])
        points.append((x + 4*RF, (y-2*R)+4*R*G))
        points.append((x + 4*RF*G, y+2*R+(2*R*(1-G))))

        points.append(self.outer[4])
        points.append((x - 4*RF*(1-G), y-2*R-(4*R*G)/2))
        points.append((x + 4*RF*(1-G), y-2*R-(4*R*G)/2))

        points.append(self.outer[2])
        points.append((x - 4*RF*G, y+2*R+(2*R*(1-G))))
        points.append((x - 4*RF, (y-2*R)+4*R*G))
        points.append(self.outer[0])

        points.append((None, None))

        points.append(self.outer[3])
        points.append((x - 4*RF, (y+2*R)-4*R*G))
        points.append((x - 4*RF*G, y-2*R-(2*R*(1-G))))

        points.append(self.outer[1])
        points.append((x + 4*RF*(1-G), y+2*R+(4*R*G)/2))        
        points.append((x - 4*RF*(1-G), y+2*R+(4*R*G)/2))

        points.append(self.outer[5])
        points.append((x + 4*RF*G, y-2*R-(2*R*(1-G))))
        points.append((x + 4*RF, (y+2*R)-4*R*G))
        points.append(self.outer[3])
        
 






        
            
        return points
        
    def build_circles(self):
        for x, y in self.points:
            #pass
            self.canvas.create_oval((x-R, y-R, x+R, y+R))

    def draw_lines(self):
        for x1, y1 in self.points:
            for x2, y2 in self.points:
                if x1 == x2 and y1 == y2:
                    continue
                self.canvas.create_line((x1, y1, x2, y2))

    def draw_golden_lines(self):
        points = iter(self.golden_points)

        #for x, y in self.golden_points:
        #    if x is None:
        #        continue
        #    self.canvas.create_oval((x-10, y-10, x+10, y+10))

        x1, y1 = points.next()
        while 1:
            try:
                x2, y2 = points.next()
                if x2 is None:
                    x1, y1 = points.next()
                    continue
                self.canvas.create_line((x1, y1, x2, y2))
                x1, y1 = x2, y2
            except StopIteration:
                break

    def post(self, event=None):
        self.canvas.postscript(file='foo.ps')
        


def main():
    root = MainWindow()
    root.mainloop()
    
    


main()
