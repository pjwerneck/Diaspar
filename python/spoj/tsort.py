from sys import stdin

stdin.readline()
d = map(int, stdin.read(-1)[::-1].split())

    
def insertionsort(A, start=0, n=None):
    if n is None: n = len(A)
    for i in xrange(1, n):
        i+= start
        v = A[i]
        j = i-1
        while j >= 0 and A[j] > v:
            A[j + 1] = A[j]
            j -= 1
        A[j + 1] = v
    return A


def permute(i, n=3):
    yield i
    k = n-1
    m = n-1
    while k > 0:
        while k>0 and i[k] <= i[k-1]:
            k -= 1
        k -= 1

        m = n-1
        while m > k and i[m] <= i[k]:
            m -= 1

        i[k], i[m] = i[m], i[k]

        n -= 1
        k += 1

        while n > k:
            i[n], i[k] = i[k], i[n]
            k += 1
            n -= 1

        yield i
    

def median(data, start, n):
    i = [start, start+n-1, start+(n/2)]

    for a, b, c in permute(i):
        if (data[a] <= data[b] <= data[c]) or (data[a] >= data[b] >= data[c]):
            return b
 
def quicksort(data, start=0, n=None):
    if n is None:
        n = len(data)

    if n <= 15:
        return insertionsort(data, start, n)

    end = start+n-1
    low = start
    high = end

    mid = 0#random.randint(start, end);


    # save pivot
    pivot = data[mid]
    
    # save low bound at the pivot
    data[mid] = data[low]

    while low < high:
        # check for low data on high side
        while (data[high] > pivot) and (low < high):
            high -= 1

        # found something?
        if high != low:
            # yes!
            data[low] = data[high]
            low += 1

        # repeat for high data on low side
        while (data[low] < pivot) and (low < high):
            low += 1

        # found something?
        if high != low:
            # yes!
            data[high] = data[low]
            high -= 1

    # put the saved value back
    data[low] = pivot

    # make the recursive call for each side
    quicksort(data, start, low-start)
    quicksort(data, low+1, end-low)

    return data

quicksort(d)

print '\n'.join(d)[::-1]
