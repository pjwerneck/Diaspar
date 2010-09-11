





for n in (10, 20, 30):
    x = [0] * n
    m = 1
    while m < 2*n:
        for dist in ('sawtooth', 'rand', 'stagger', 'plateau', 'shuffle'):
            i = j = 0
            k = 1
            while i < n:
                if dist == 'sawtooth':
                    x[i] = i % m

                    
                i += 1

            print dist, x
        m *= 2
