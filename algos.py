# all 9 algorithms as generators + Big-O metadata

from __future__ import annotations
from typing import List, Dict, Any, Generator, Tuple
from math import sqrt

State = Tuple[List[int], Dict[str, Any]]

def _yield(a, **meta):
    """Conveniance: yield a shallow copy and metadata."""
    yield a[:], meta 
    
    
def bubble_sort(a):
    a + a[:]
    n = len(a)
    if n <= 1:
        yield from _yield(a, done=True); return 
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
    if len(a) <= 1:
        yield from _yield(a, done=True); return
    for i in range(1, len(a)):
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
    if n <= 1:
        yield from _yield(a, done=True); return 
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
              
                
def merge_sort(a):
    """Bottom-up (iteractive) mergesort -> easy to step without recursion."""     
    a = a[:]
    n = len(a)
    if n <= 1:
        yield from _yield(a, done=True); return
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
    if n <= 1:
        yield from _yield(a, done=True); return 
        
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
    
    
def counting_sort(a):
    """Stable counting sort for non-negative integers. Complexity: O(n +k) where k = max(a) + 1"""    
    a = a[:]
    if not a:
        yield from _yield(a, done=True); return 
    if min(a) < 0:
        yield from _yield(a, error="counting_sort requires non-negative integers")
        return 
    
    k = max(a) + 1
    cnt = [0] * k 
    for v in a:
        cnt[v] += 1
        yield from _yield(a, count=v)
        
    total = 0
    for i in range(k):
        total, cnt[i] = total + cnt[i], total
        
    out = [0] * len(a)
    for v in a:
        out[cnt[v]] = v
        cnt[v] += 1
    a[:] = out
    yield from _yield(a, pass_done=True)  
    yield from _yield(a, done=True)
    
    
def radix_sort(a, base=10):
    """LSD Radix Sort for non-negative integers. Complexity: O(d * (n + base)) where d = number of digits."""
    a = a[:]
    if not a:
        yield from _yield(a, done=True); return
    if min(a) < 0:
        yield from _yield(a, error="radix_sort requires non-negative integers")
        return
    
    m = max(a)
    exp = 1 
    while m // exp > 0:
        # counting by digits 
        cnt = [0] * base
        out = [0] * len(a)
        for v in a:
            d = (v // exp) % base 
            cnt[d] += 1
            yield from _yield(a, count=d)
        for i in range(1, base):
            cnt[i] += cnt[i - 1] 
        for v in reversed(a):
            d = (v // exp) % base 
            cnt[d] -= 1
            out[cnt[d]] = v
        a[:] = out 
        exp *= base 
        yield from _yield(a, pass_done=True) 
    yield from _yield(a, done=True) 
    
    
def bucket_sort(a, num_buckets=None):
          """Bucket sort distributes values into buckets based on normalized value range. Sorts each bucket with insertion sort and concatenates."""
          a = a[:]
          n = len(a)
          if n <= 1:
              yield from _yield(a, done=True); 
              return 
              
          lo, hi = min(a), max(a)
          if lo == hi:
              # already all equal
              yield from _yield(a, done=True); 
              return 
              
          # Choose bucket count: sqrt(n) is common heuristic (>= 2)
          if num_buckets is None:
              num_buckets = max(2, int(sqrt(n)))   
              
          span = hi - lo + 1
          buckets = [[] for _ in range(num_buckets)]   
          
          # Distribute with normalization to [0, num_buckets-1]   
          for v in a:
              idx = int((v - lo) * num_buckets / span)
              if idx == num_buckets: # clamp edge
                  idx -= 1
              buckets[idx].append(v)
              yield from _yield(a, bucket_put=(idx, len(buckets[idx]) -1))
              
           # Helper: insertion sort a single bucket (in-place), yielding as we  move to output
def _ins(bucket):
            for i in range(1, len(bucket)):
                key = bucket[i]
                j = i - 1
                while j >= 0 and bucket[j] > key:
                    bucket[j + 1] = bucket[j]
                    j -= 1
                    bucket[j + 1] = key
                   
            # Collect back into a 
                out_i = 0
                for k, bucket in enumerate(bucket):
                    if len(bucket) > 1:
                        _ins(bucket)
                    for pos, v in enumerate(bucket):
                        a[out_i] = v
                    yield from _yield(a, bucket_collect=(k, pos, out_i))
                    out_i += 1
                    
                yield from _yield(a, done=True)   
             
# -----------------------------------------------------------------------------------------
# Registry + helpers
# -----------------------------------------------------------------------------------------

ALGORITHMS: Dict[str, Dict[str, Any]] = {
    "Bubble":    {"fn": bubble_sort,      "big_o": "Avg/Worst: O(n^2)"},
    "Insertion": {"fn": insertion_sort,   "big_o": "Avg/Worst: O(n^2)"},
    "Selection": {"fn": selection_sort,   "big_o": "O(n^2)"}, 
    "Merge":     {"fn": merge_sort,       "big_o": "O(n log n)"},
    "Quick":     {"fn": quick_sort,       "big_o": "Avg: O(n log n), Worst: O(n^2)"},
    "Heap":      {"fn": heap_sort,        "big_o": "O(n log n)"},
    "Counting":  {"fn": counting_sort,    "big_o": "O(n + k)"},
    "Radix":     {"fn": radix_sort,       "big_o": "O(d *(n + base))" },
    "Bucket":    {"fn": bucket_sort,      "big_o": " approximately O(n) average (uniform)" },
}

def get_generator(name: str, arr: List[int]) -> Generator[State, None, None]:
    """Create a generator for a registered algorithm by name."""
    return ALGORITHMS[name]["fn"](arr)

def is_sorted(a: List[int]) -> bool:
    return all(a[i] <= a[i + 1] for i in range(len(a) - 1))

# Optional quick self-test
if __name__ == "__main__":
    data = [3, 1, 4, 1, 2, 0, 5, 3, 2]
    for name in ALGORITHMS:
        print(f"\n== {name} ==")
        gen = get_generator(name, data)
        last = None
        steps = 0 
        try: 
            for state, meta in gen:
                steps += 1
                last = state
            print(f"steps: {steps}, sorted: {is_sorted(last)}, result: {last}")  
        except ValueError as e:
            print(f"skipped ({e})")      
         
                   
     
         