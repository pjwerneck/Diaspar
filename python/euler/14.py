

cache = {}



def seq(n):
    
    m = [n]
    while m[-1] != 1:
        d = m[-1]
        if d in cache:
            #print d, 'from cache'
            m.extend(cache[d])
            continue

        if d % 2:
            m.append(3*d + 1)

        else:
            m.append(d/2)

    cache[n] = m[1:]
    return m

msofar = 0
saved = None

for x in range(1, 1000000):
    m = len(seq(x))
    if m > msofar:
        msofar = m
        saved = x

print msofar, saved
    
