

from __future__ import division

import math



L1 = 8
L2 = 10

Lmax = L1 + L2
Lmin = L1 - L2



def angle_to_coords(A, B):
    x1 = math.cos(math.radians(A)) * L1
    y1 = math.sin(math.radians(A)) * L1

    x2 = math.sin(math.radians(B)) * L2 + x1
    y2 = y1 - math.cos(math.radians(B)) * L2

    x1 -= 2
    x2 -= 2
    y1 += 7
    y2 += 7
    
    return x1, y1, x2, y2


def calcpos(x1, y1):
    x0 = 0
    y0 = 0
    r0 = L1
    r1 = L2
    # dx and dy ae the vertical and horizontal distances between circles
    dx = x1 - x0
    dy = y1 - y0

    # d is the line between P0 and P2
    d = math.hypot(dx, dy)

    print "d =", d

    if d > Lmax:
        return "UNREACHABLE"
    if d == 0:
        return "UNREACHABLE"
    if d < Lmin:
        return "UNREACHABLE"

    r0 = L1
    r1 = L2

    # P2 is where the two circle intersections cross d
    # a is the distance from P0 to P2    
    a = ((r0*r0) - (r1*r1) + (d*d)) / (2.0 * d)
    b = d-a
    print "a = ", a
    print "b = ", b

    # P2 coords
    x2 = x0 + (dx * a/d)
    y2 = y0 + (dy * a/d)

    # h is the distance from p2 to the intersections
    h = math.sqrt((r0*r0) - (a*a))
    print "h = ", h

    # determine the offsets of the intersections to point 2
    rx = -dy * (h/d)
    ry = dx * (h/d)

    # determine the intersections
    xa = x2 + rx
    ya = y2 + ry

    xb = x2 - rx
    yb = y2 - ry

    #    return xa, ya

    q1 = math.atan2(y1, x1)
    q2 = math.acos((L1*L1 - L2*L2 + d*d)/(2*L1*d))
    

    # for angle A, first joint
    A = math.degrees(q1+q2)
    B = math.degrees(math.acos((L1*L1 + L2*L2 - d*d) / (2*L1*L2)))
    return A, B


def main1():
    while 1:
        A = raw_input("A: ")
        B = raw_input("B: ")


def main2():
    print calcpos(12, 5)


main2()
