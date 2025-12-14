import math
import time
import sys

# Increase recursion depth just in case, though not strictly needed for this iterative approach
sys.setrecursionlimit(2000)

# --- 1. PRIMALITY TESTS ---

def wilsons_theorem_check(j):
    """
    Checks if j is prime using Wilson's Theorem: (j-1)! = -1 (mod j)
    Time Complexity: O(j) per check (iterative modular factorial).
    """
    if j < 2: return False
    fact = 1
    for i in range(1, j):
        fact = (fact * i) % j
    return (fact + 1) % j == 0

def miller_rabin_deterministic(n):
    """
    Deterministic Miller-Rabin primality test for n < 2^64.
    Time Complexity: O(k * log^3 n), where k is number of bases (12).
    """
    if n < 2: return False
    if n == 2 or n == 3: return True
    if n % 2 == 0: return False

    # Bases for deterministic correctness up to 2^64
    bases = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    
    # Decompose n-1 into d * 2^r
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    for a in bases:
        if a >= n: break
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

# --- 2. THE ALGORITHMS ---

def original_willans_formula(n):
    """
    Finds nth prime using the logic of Willans' Formula.
    - Upper Bound: 2^n
    - Prime Check: Wilson's Theorem
    """
    upper_bound = 2**n
    prime_count = 0
    
    # Willans' formula effectively sums 1 for every integer m where pi(m) < n
    # We simulate this by iterating and counting.
    current_integer = 1
    while current_integer <= upper_bound:
        if wilsons_theorem_check(current_integer):
            prime_count += 1
        
        if prime_count == n:
            return current_integer
        
        current_integer += 1
    return -1 # Should not reach here

def hybrid_rosser_dmr(n):
    """
    Finds nth prime using the Optimized Hybrid Approach.
    - Upper Bound: Rosser's Theorem (n log n + n log log n)
    - Prime Check: Deterministic Miller-Rabin
    """
    if n == 1: return 2
    
    # Rosser's Upper Bound (valid for n >= 6, we pad slightly for small n)
    if n < 6:
        limit = 15 # Hardcoded safety for tiny n
    else:
        log_n = math.log(n)
        limit = int(n * (log_n + math.log(log_n))) + 2 # +2 for safety margin
        
    prime_count = 0
    current_integer = 1
    
    # Scan within the reduced Rosser range
    while current_integer <= limit:
        current_integer += 1
        if miller_rabin_deterministic(current_integer):
            prime_count += 1
            if prime_count == n:
                return current_integer
            
    return -1

# --- 3. BENCHMARK ---

def run_benchmark():
    print(f"{'n':<5} | {'True Pn':<10} | {'Original (sec)':<15} | {'Hybrid (sec)':<15} | {'Speedup':<10}")
    print("-" * 65)
    
    # Testing small n because Original Willans explodes in complexity very fast
    test_values = [1, 2, 3, 20, 21, 22, 51, 79, 104, 229, 1031, 1355, 1900, 3044] 
    
    for n in test_values:
        # Measure Hybrid
        start_h = time.perf_counter()
        p_hybrid = hybrid_rosser_dmr(n)
        time_h = time.perf_counter() - start_h
        
        # Measure Original (Only if n is small enough to finish in reasonable time)
        if n <= 4000: 
            start_o = time.perf_counter()
            p_orig = original_willans_formula(n)
            time_o = time.perf_counter() - start_o
            speedup = f"{time_o / time_h:.1f}x"
        else:
            p_orig = "TIMEOUT"
            time_o = float('inf')
            speedup = "Inf"

        # Format output
        t_o_str = f"{time_o:.6f}" if isinstance(time_o, float) and time_o != float('inf') else "SKIPPED"
        print(f"{n:<5} | {p_hybrid:<10} | {t_o_str:<15} | {time_h:.6f}          | {speedup}")

if __name__ == "__main__":
    print("Benchmarking Original Willans vs. Hybrid Rosser-DMR...")
    print("Note: Original Willans uses Wilson's Thm (O(j)) and 2^n bound.")
    print("This will get incredibly slow past n=9.\n")
    run_benchmark()
