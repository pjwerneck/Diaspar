



def lcm(a, b):
    lower = min([a, b])

    t = lower

    while 1:
        if t % a or t % b:
            t += lower
            continue
        break
    return t

    
    



print reduce(lcm, range(1, 21))
    
