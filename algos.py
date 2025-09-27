# all 9 algorithms as generators + Big-O metadata
import time 
from typing import List, Geneterator, Tuple, Dict, Any

def bubble_sort(data: List[int]) -> Generator:
    a = data[:]
    steps = comps = swaps = 0 
    start_time = time.time()
    n = len(a)
    
    for i in range(n):
        for j in range(0, n - i - 1):
            comps += 1
            meta = {"steps": steps, "comparisons": comps, "swaps": swaps, "compare": (j, j+1), "time": time.time() - start_time}
            yield a[:], meta
            
            if a[j] > a[j+1]:
                a[j], a[j+1] = a[j+1], a[j]
                swaps += 1
                steps += 1
                meta = {"steps": steps, "comparisons": comps, "swaps": swaps, "swap": (j, j+1), "time": time.time() - start_time}
                yield a[:], meta 
                
    meta = {"steps": steps, "comparisons": comps, "swaps": swaps, "done": True, "time": time.time() - start_time}
    yield a[:], meta
    
    
def insertion_sort_gen(data: List[int]) -> Generator:
    """Insertion sort that yields each step"""
    a = data[:]
    steps = comps = swaps = 0 
    start_time = time.time()
        
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
            
        while j >= 0:
            comps += 1
            meta = {"steps": steps, "comparisons": comps, "swaps": swaps, "compare": (j, j+1), "time": time.time() - start_time}
            yield a[:], meta 
                
            if a[j] > key:
                a[j+1] = a[j]
                steps += 1
                j -= 1
                meta = {"steps": steps, "comparisons": comps, "swaps": swaps, "swap": (j+1, j+2), "time": time.time() - start_time}
                yield a[:], meta
            else:
                break
                
            a[j+1] = key 
            steps += 1
            
        meta = {"steps": steps, "comparisons": comps, "swaps": swaps, "done": True, "time": time.time() - start_time}
        yield a[:], meta
        
def merge_sort_gen(data: List[int]) -> Generator:
    """Merge sort that yields each step"""
    a = data[:]
    steps = comps = swaps = 0 
    start_time = time.time()
    
    def merge(left, mid, right):
        nonlocal steps, comps, swaps
        L = a[left:mid+1]
        R = a[mid+1:right+1]
        i = j = 0 
        k = left
        
        while i < len(L) and j < len(R):
            comps += 1
            meta = {"steps": steps, "comparisons": comps, "swaps": swaps, "compare": (left + i, mid + 1 + j), "time": time.time() - start_time}
            yield a[:], meta
            
            if L[i] <= R[j]:
                a[k] = L[i]
                i += 1
                
            else:
                a[k] = L[i]
                j += 1
            k += 1
            steps += 1
            yield a[:], {"steps": steps, "comparisons": comps, "swaps": swaps, "time": time.time() - start_time}
            
        while i < len(L):
            a[k] = L[i]
            i += 1
            k += 1
            steps += 1
            yield a[:], {"steps": steps, "comparisons": comps, "swaps": swaps, "time": time.time() - start_time}
            
        while j < len(R):
            a[k] = R[j]
            j += 1
            k += 1
            steps += 1
            yield a[:], {"steps": steps, "comparisons": comps, "swaps": swaps, "time": time.time() - start_time}
    
    def mergesort(left, right):
         if left< right:
             mid = (left + right) // 2
             yield from mergesort(left, mid)
             yield from mergesort(mid + 1, right)
             yield from merge(left, mid, right)
    
    if len(a) > 1:
        yield from mergesort(0, len(a) - 1)
        
    meta = {"steps": steps, "comparisons": comps, "swaps": swaps, "done": True, "time": time.time() - start_time}
    yield a[:], meta  
    
def quick_sort_gen(data: List[int]) -> Generator: 
    """Quick sort that yields each step"""  
    a = data[:]
    steps = comps = swaps = 0 
    start_time = time.time()
    
    def partition(low, high):
        nonlocal steps, comps, swaps
        pivot = a[high]
        i = low - 1
        
        for j in range(low, high):
            comps += 1
            if i != j:
                a[i], a[j] = a[j], a[i]
                swaps += 1
                steps += 1
                meta = {"steps": steps, "comparisons": comps, "swaps": swaps, "swap": (i, j), "time": time.time() - start_time}
                yield a[:], meta
                
        if i + 1 != high:
            a[i + 1], a[high] = a[high], a[i + 1]
            swaps += 1
            steps += 1
            meta = {"steps": steps, "comparisons": comps, "swaps": swaps, "swap": (i + 1, high), "time": time.time() - start_time}
            yield a[:], meta
            
        return i + 1
    
    def quicksort(low, high):
        if low < high:
            gen = partition(low, high)
            pi = None
            for state, meta in gen:
                yield state, meta
                if "swap" in meta and meta["swap"][i] == high:
                    pi = meta["swap"][0]
                    
            if pi is None:
                pi = high
                
            yield from quicksort(low, pi - 1)
            yield from quicksort(pi + 1, high)
            
    if len(a) > 1:
        yield from quicksort(0, len(a) - 1)
        
    meta = {"steps": steps, "comparisons": comps, "swaps": swaps, "done": True, "time": time.time() - start_time}
    yield a[:], meta
    
def heap_sort_gen(data: List[int]) -> Generator:
    """Heap sort that yields each step"""
    a = data[:]
    steps = comps = swaps = 0 
    start_time = time.time()
    n = len(a)
    
    def heapify(n, i):
        nonlocal steps, comps, swaps
        largest = i 
        l = 2 * i + 1
        r = 2 * i + 2
        
        if l < n:
            comps += 1
            meta = {"steps": steps, "comparisons": comps, "swaps": swaps, "compare": (largest, l), "time": time.time() - start_time}
            yield a[:], meta
            if a[l] > a[largest]:
                largest = l
                
        if r < n:
            comps += 1
            meta = {"steps": steps, "comparisons": comps, "swaps": swaps, "compare": (largest, r), "time": time.time() - start_time}
            yield a[:], meta
            if a[r] > a[largest]:
                largest = r
                
        if largest != i:
            a[i], a[largest] = a[largest], a[i]
            swaps += 1
            steps += 1
            meta = {"steps": steps, "comparisons": comps, "swaps": swaps, "swap": (i, largest), "time": time.time() - start_time}
            yield a[:], meta
            yield from heapify(n, largest)
            
    # Build heap
    for i in range(n // 2 - 1, -1, -1):
        yield from heapify(n, i)
        
    # Extract elements 
    for i in range(n - 1, 0, -1):
        a[0], a[i] = a[i], a[0]
        swaps += 1
        steps += 1
        meta = {"steps": steps, "comparisons": comps, "swaps": swaps, "swap": (0, i), "time": time.time() - start_time}
        yield a[:], meta
        yield from heapify(i, 0)
        
    meta = {"steps": steps, "comparisons": comps, "swaps": swaps, "done": True, "time": time.time() - start_time}
    yield a[:], meta
    
def counting_sort_gen(data: List[int]) -> Generator:
    """Counting sort that yields each step"""
    a = data[:]
    steps = comps = swaps = 0
    start_time = time.time()
    
    if not a:
        yield a[:], {"steps": 0, "comparisons": 0, "swaps": 0, "done": True, "time": 0}
        return
    
    # Find range
    max_val = max(a)
    min_val = min(a)
    range_val = max_val - min_val + 1
    
    
    # Count occurences 
    count = [0] * range_val
    for i, val in enumerate(a):
        count[val - min_val] += 1
        steps += 1
        meta = {"steps": steps, "comparisons": comps, "swaps": swaps, "highlight": [i], "time": time.time() - start_time}
        yield a[:], meta
        
        
    # Reconstruct array 
    output = [0] * len(a)
    idx = 0 
    for i in range(range_val):
        while count[i] > 0:
            output[idx] = i + min_val
            count[i] -= 1
            idx += 1
            steps += 1
            # Update original array to show progress
            a[:idx] = output[:idx]
            meta = {"steps": steps, "comparisons": comps, "swaps": swaps, "highlight": [idx-1], "time": time.time() - start_time}
            yield a[:], meta
            
    meta = {"steps": steps, "comparisons": comps, "swaps": swaps, "done": True, "time": time.time() - start_time}
    yield a[:], meta
    
def radix_sort_gen(data: List[int]) -> Generator:
    """Radix sort that yields each step"""
    a = data[:]
    steps = comps = swaps = 0
    start_time = time.time()
    
    if not a :
        yield a[i], {"steps": 0, "comparisons": 0, "swaps": 0, "done": True, "time": 0}
        return
    
    max_val = max(a)
    exp = 1
    
    while max_val // exp > 0:
        # Counting sort for current digit
        output = [0] * len(a)
        count = [0] * 10
        
        # Count occurances of each digit 
        for i in range(len(a)):
            index = (a[i] // exp) % 10
            count[index] += 1
            steps += 1
            meta = {"steps": steps, "comparisons": comps, "swaps": swaps, "highlight": [i], "time": time.time() - start_time}
            yield a[:], meta
            
        # Change count[i] to actual position 
        for i in range(1, 10):
            count[i] += count[i - 1]
            
        # Build output array
        for i in range(len(a)- 1, -1, -1):
            index = (a[i] // exp) % 10
            output[count[index] - 1] = a[i]
            count[index] -= 1
            steps += 1
            
        # Copy output array to original array 
        for i in range(len(a)):
            a[i] = output[i]
            meta = {"steps": steps, "comparisons": comps, "swaps": swaps, "highlight": [i], "time": time.time() - start_time}
            yield a[:], meta
        
        exp *= 10
    
    meta = {"steps": steps, "comparisons": comps, "swaps": swaps, "done": True, "time": time.time() - start_time}
    yield a[:], meta
    
def bucket_sort_gen(data: List[int]) -> Generator:
    """Bucket sort that yields each step"""
    a = data[:]
    steps = comps = swaps = 0
    start_time = time.time()
    
    if len(a) <= 1:
        yield a[:], {"steps": 0, "comparisons": 0, "swaps": 0, "done": True, "time": 0}
        return
    
    # Create buckets
    bucket_count = len(a)
    max_val = max(a)
    min_val + min(a)
    range_val = max_val - min_val + 1
    
    buckets = [[] for _ in range(bucket_count)]
    
    # Distribute elements into buckets
    for i, val in enumerate(a):
        bucket_index = min(bucket_count - 1, (val - min_val) * bucket_count // range_val)
        buckets[bucket_index].append(val)
        steps += 1
        meta = {"steps": steps, "comparisons": comps, "swaps": swaps, "highlight": [i], "time": time.time() - start_time}
        yield a[:], meta
        
    # Sort individual buckets and concentrate
    result = []
    for bucket in buckets:
        if bucket:
            bucket.sort() # Using built-in sort for simplicity 
            result.extend(bucket)
            
    # Copy back to original array
    for i, val in enumerate(result):
        a[i] = val 
        steps += 1
        meta = {"steps": steps, "comparisons": comps, "swaps": swaps, "highlight": [i], "time": time.time() - start_time}
        yield a[:], meta
    
    meta = {"steps": steps, "comparisons": comps, "swaps": swaps, "done": True, "time": time.time() - start_time}
    yield a[:], meta
    
def quick_select_sort_gen(data: List[int]) -> Generator:
    """Quick select adapted for sorting (essentially quicksort)"""
    
    a = data[:]
    steps = comps = swaps = 0
    start_time = time.time()
    
    def partition(low, high):
        nonlocal steps, comps, swaps
        pivot = a[high]
        i = low - 1
        
        for j in range(low, high):
            comps += 1
            meta = {"steps": steps, "comparisons": comps, "swaps": swaps, "compare": (j, high), "time": time.time() - start_time}
            yield a[:], meta
            
            if a[j] <= pivot:
                i += 1
                if i != j:
                    a[i], a[j] = a[j], a[i]
                    swaps += 1
                    steps += 1
                    meta = {"steps": steps, "comparisons": comps, "swaps": swaps, "swap": (i, j), "time": time.time() - start_time}
                    yield a[:], meta
                    
        if i + 1 != high:
            a[i + 1], a[high] = a[high], a[i + 1]
            swaps += 1
            steps += 1
            meta = {"steps": steps, "comparisons": comps, "swaps": swaps, "swap": (i + 1, high), "time": time.time() - start_time}
            yield a[:], meta
        
        return i + 1
    
    def quickselect_sort(low, high):
        if low < high:
            gen = partition(low, high)
            pi = None
            for state, meta in gen:
                yield state, meta
                if "swap" in meta and meta["swap"][1] == high:
                    pi = meta["swap"][0]
                    
            if pi is None:
                pi = high
                
            yield from quickselect_sort(low, pi - 1)
            yield from quickselect_sort(pi + 1, high)
            
    if len(a) > 1:
        yield from quickselect_sort(0, len(a) - 1)
    
    meta = {"steps": steps, "comparisons": comps, "swaps": swaps, "done": True, "time": time.time() - start_time}
    yield a[:], meta
    
def get_generator(name: str, data: List[int]):
    """Get sorting algorithm generator by name"""
    if "Bubble" in name:
        return bubble_sort_gen(data)
    elif "Insertion" in name:
        return insertion_sort_gen(data)
    elif "Merge" in name:
        return merge_sort_gen(data)
    elif "Quick Sort" in name:
        return quick_sort_gen(data)
    elif "Heap" in name:
        return heap_sort_gen(data)
    elif "Counting" in name:
        return counting_sort_gen(data)
    elif "Radix" in name:
        return radix_sort_gen(data)
    elif "Bucket" in name:
        return bucket_sort_gen(data)
    elif "Quick Select" in name:
        return quick_select_sort_gen(data)
    else:
        # Default to bubble sort for unimplemented algorithms
        return bubble_sort_gen(data)
    