
import random
import math
import timeit
import heapq

N = 100


# Insertion sort

def insertionsort(A):
    for i in xrange(1, len(A)):
        v = A[i]
        j = i-1
        while j >= 0 and A[j] > v:
            A[j + 1] = A[j]
            j -= 1
        A[j + 1] = v
    return A

def test_insertionsort():
    D = range(N)
    random.shuffle(D)
    assert insertionsort(D) == range(N)
    

# Selection sort

def selectionsort(A):
    n = len(A)
    for i in range(n-1):
        m = i
        for j in range(i+1, n):
            if A[j] < A[m]:
                m = j
        A[i], A[m] = A[m], A[i]

    return A

def test_selectionsort():
    D = range(N)
    random.shuffle(D)
    assert selectionsort(D) == range(N)
    

# Mergesort

def merge(left, right):
    if not left:
        return right
    if not right:
        return left

    result = []            
    while (left and right):
        if left[0] <= right[0]:
            result.append(left.pop(0))
        else:
            result.append(right.pop(0))

    if left:
        result.extend(left)
    if right:
        result.extend(right)

    return result

def _merge(left, right):
    # I'm cheating... technically, I'm doing a heapsort here
    result = left + right
    heapq.heapify(result)
    return [heapq.heappop(result) for n in xrange(len(result))]


def mergesort(A):
    n = len(A)
    if n <= 1:
        return A
    if n <= 30:
        return insertionsort(A)
    else:
        m = n // 2
        right = A[m:]
        result = merge(mergesort(A[:m]), mergesort(A[m:]))
        return result


def test_mergesort():
    D = range(N)
    random.shuffle(D)
    assert mergesort(D) == range(N)
    

# Quicksort
            
def quicksort(A):
    if len(A) <= 1:
        return A
    pivot = A[len(A)/2]

    less = [x for x in A if x < pivot]
    equal = [x for x in A if x == pivot]
    greater = [x for x in A if x > pivot]
    
    return quicksort(less) + equal + quicksort(greater)
        
def test_quicksort():
    D = range(N)
    random.shuffle(D)
    assert quicksort(D) == range(N)
    

# Heapsort

def heapify(A, count):
    start = (count - 1) / 2
    while start >= 0:
        siftdown(A, start, count-1)
        start = start - 1

def siftdown(A, start, end):
    root = start
    while root * 2 + 1 <= end:
        child = root * 2 + 1
        if child < end and A[child] < A[child+1]:
            child = child + 1
        if A[root] < A[child]:
            A[root], A[child] = A[child], A[root]
            root = child
        else:
            break

def heapsort(A):
    count = len(A)
    heapify(A, count)

    end = count - 1
    while end > 0:
        A[end], A[0] = A[0], A[end]
        end = end - 1
        siftdown(A, 0, end)
    return A

def test_heapsort():
    D = range(N)
    random.shuffle(D)
    assert heapsort(D) == range(N)
    

# Bubblesort

def bubblesort(A):
    while 1:
        swap = 0

        for i in range(len(A)-1):
            j = i + 1
            if A[i] > A[j]:
                A[j], A[i] = A[i], A[j]
                swap = 1

        if not swap:
            break

    return A

def test_bubblesort():
    D = range(N)
    random.shuffle(D)
    assert bubblesort(D) == range(N)
    

# Cocktailsort

def cocktailsort(A):
    while 1:
        swap = 0

        for i in range(len(A)-1):
            j = i + 1
            if A[i] > A[j]:
                A[j], A[i] = A[i], A[j]
                swap = 1

        for i in reversed(range(len(A)-1)):
            j = i + 1
            if A[i] > A[j]:
                A[j], A[i] = A[i], A[j]
                swap = 1

        if not swap:
            break
        
    return A

def test_cocktailsort():
    D = range(N)
    random.shuffle(D)
    assert cocktailsort(D) == range(N)
    

# Strandsort

def strandsort(A):
    results = []
    while A:
        sublist = [A.pop(0)]
        i = 0
        while i < len(A):
            if A[i] > sublist[-1]:
                sublist.append(A.pop(i))
            i += 1

        results = merge(results, sublist)

    A[:] = results
    #return results
    
def test_strandsort():
    N = 2 ** 13
    D = range(N)
    random.shuffle(D)
    strandsort(D)
    assert D == range(N)
    

# Combsort

# basegap -> 1/(1-1/(e**phi))
BASEGAP = 1/(1-(1/(math.e**((1+math.sqrt(5))/2))))

def combsort(A):
    gap = len(A)
    swap = 1

    while gap > 1 and swap:
        if gap > 1:
            gap = int(gap / BASEGAP)

        i = 0
        swap = 0
        while i + gap < len(A):
            igap = i + gap
            if A[i] > A[igap]:
                A[i], A[igap] = A[igap], A[i]
                swap = 1
            i += 1
    return A
            
def test_combsort():
    D = range(N)
    random.shuffle(D)
    combsort(D)
    assert D == range(N)
    

    


def main():

    
    
    print 'insertionsort, %.2f usec/pass'%(10000 * timeit.Timer('test_insertionsort()', 'from __main__ import test_insertionsort').timeit(number=10000) / 10000)
    print 'cocktailsort, %.2f usec/pass'%(10000 * timeit.Timer('test_cocktailsort()', 'from __main__ import test_cocktailsort').timeit(number=10000) / 10000)
    #print 'mergesort, %.2f usec/pass'%(10000 * timeit.Timer('test_mergesort()', 'from __main__ import test_mergesort').timeit(number=10000) / 10000)

    
    #test_insertionsort()
    #test_selectionsort()
    #test_mergesort()
    #test_quicksort()
    #test_heapsort()
    #test_bubblesort()
    #test_cocktailsort()
    #test_strandsort()
    #test_combsort()

    

if __name__ == '__main__':
    main()
