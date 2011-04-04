
import math





def check(n):
    t = int(math.sqrt(n))

    divs = []
    
    while t > 0:
        d, m = divmod(n, t)
        if m:
            t -= 1
            continue
        divs.append((d, t))
        print d, t

        t -= 1
    
    return divs
        
T = 600851475143


check(T)
