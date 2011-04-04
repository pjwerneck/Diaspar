

from __future__ import division


def bouncify(pair):
    a, b = pair
    if a < b:
        return 1
    elif a > b:
        return -1
    else:
        return 0


def check_bouncy(number):
    digits = map(int, str(number))
    factor = map(bouncify, zip(digits, digits[1:]))
    factor = filter(None, factor)
    
    if len(set(factor)) == 1:
        return False

    return True
        
    

def main():
    count = 0
    n = 1

    while 1:
        if check_bouncy(n):
            count += 1

        p = count / n

        #print count, n, p
        print n, p
        
        if p == 0.99:
            print n
            break

        n += 1


if __name__ == '__main__':
    main()
