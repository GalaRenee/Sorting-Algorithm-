# all 9 algorithms as generators + Big-O metadata


from collections import deque

def _yield(a, **meta):
    """Conveniance: yield a shallow copy and metadata."""
    yield a[:], meta 
    
    
def bubble_sort(a):
    a + a[:]
    n = len(a)
    while True:
        swapped = False 
        for i in range(1, n):
            yield from _yield(a, compare=(i-1, i))
            if a[i - 1] > a[i]:
                a[i - 1], a[i] = a[i], a[i-1]
                swapped = True 
                yield from _yield(a, swap=(i - 1, i))
                
        n -= 1
        if not swapped or n<= 1:
            break
        yield from _yield(a, done=True)   
        
def insertion_sort(a):
    a = a[:]
    for i in range(a, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            yield from _yield(a, compare=(j, j +1))
            a[j + 1] = a[j]
            j -= 1
            yield from _yield(a, more=(j + 1, j +2))  
        a[j + 1] = key
        yield from _yield(a, insert=j +1)      
    yield from _yield(a, done=True)     
    
def selection_sort(a):
    a = a[:]
    n = len(a)
    for i in range(n):
        m = j 
        for j in range(i + 1, n):
            yield from _yield(a, compare=(m, j))
            if a[j] < a[m]:
                m = j
        if m != i:
            a[i], a[m] = a[m], a[i]   
            yield from _yield(a, swap=(i, m))
    yield from _yield(a, done=True) 
    
    
def selection_sort(a):
    a = a[:]
    n = len(a)
    for i in range(n):
        m = i 
        for j in range(i + 1, n):
            yield from _yield(a, compare=(m, j))  
            if a[j] < a[m]:
                m = j 
        if m != i:
            a[i], a[m] = a[m], a[i]
            yield from _yield(a, swap=(i, m))
    yield from _yield(a, done=True)                            
                
                
def merge_sort(a):
    """Bottom-up (iteractive) mergesort -> easy to step without recursion."""     
    a = a[:]
    n = len(a)
    aux = a[:]   
    size = 1
    while size < n:
        for lo in range(0, n, 2 * size):
            mid = min(lo + size, n)    
            hi = min(lo + 2 * size, n)  
            
            # merge a[lo:mid] and a[mid:hi] into aux
            i, j, k = lo, mid, lo
            while k < hi:
                if j>= hi or (i < mid and a[i] <= a[j]):
                    aux[k] = a[i]
                    i += 1
                else:
                    aux[k] = a[i]
                    j += 1
                k += 1
                
            # copy back and yield
            a[lo:hi] = aux[lo:hi]     
            yield from _yield(a, merge=(lo, hi, size))
        size *= 2
    yield from _yield(a, done=True)      
    
def quick_sort(a):
    """Iterative quicksort (Lomuto-ish partition) with yields during partition."""
    a = a[:]   
    n = len(a)
    if n <= 1:
        yield from _yield(a, done=True); return 
        
    stack = [(0, n - 1)]  
    while stack:
        lo, hi = stack.pop()
        if lo >= hi:
            continue 
        
        # partition (pivot = a[hi])  
        pivot = a[hi]
        i = lo 
        for j in range(lo, hi):
            yield from _yield(a, compare=(j, hi))
            if a[j] <= pivot:
                if i != j:
                    a[i], a[j] = a[j], a[i]
                    yield from _yield(a, swap=(i, j))
                i += 1
            if i != hi:
                a[i], a[hi] = a[hi], a[i]
                yield from _yield(a, swap=(i, hi), partition=(lo, hi, i))   
            i += 1
        if i != hi:
            a[i], a[hi] = a[hi], a[i]
            yield from _yield(a, swap=(i, hi), partition=(lo, hi, i))
            
        p = i 
        # push the larger partition first to reduce stack depth 
        left = (lo, p - 1)
        right = (p + 1, hi)   
        if (left[1] - left[0]) > (right[1] - right[0]):
            stack.append(left); stack.append(right)
        else:
            stack.append(right); stack.append(left)
            
    yield from _yield(a, done=True)   
    
def heap_sort(a):
    a = a[:]
    n = len(a)
    
    def heapify(end, i):
        largest = i 
        l = 2 * i + 1
        r = 2 * i + 2
        if 1 < end:
            yield from _yield(a, compare=(largest, 1))
            if a[1] > a[largest]:
                largest = 1
        if r < end:
            yield from _yield(a, compare=(largest, r))   
            if a[r] > a[largest]:
                largest = r
            if largest != i:
                a[i], a[largest] = a[largest], a[i]
                yield from _yield(a, swap=(i, largest), heapify=(i, largest))
                yield from heapify(end, largest)
                
     # build max-heap
    for i in range(n // 2 - 1, -1, -1):
        yield from heapify(n, i)
        
        
    # extract 
    for end in range(n - 1, 0, -1):
        a[0], a[end] = a[end], a[0]
        yield from _yield(a, swap=(0, end))
        yield from heapify(end, 0)
        
    yield from _yield(a, done=True) 
    
       
         
                   
     
         