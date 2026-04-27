import time
import threading

# ==========================================
# Worker Function
# ==========================================
def compute_partial_squares(start_index, end_index, results, thread_id):
    """
    Thread worker: computes partial sum of squares for a slice of numbers.
    - start_index, end_index: range boundaries
    - results: shared list to store partial sums
    - thread_id: index to place result in results list
    """
    results[thread_id] = sum(i * i for i in range(start_index, end_index))

# ==========================================
# Sequential Implementation
# ==========================================
def compute_sequential(N):
    """
    Sequential sum of squares from 1 to N.
    Returns: total sum of squares
    """
    return sum(i * i for i in range(1, N + 1))

# ==========================================
# Parallel Implementation
# ==========================================
def compute_parallel(N, num_threads=4):
    """
    Parallel sum of squares using threads.
    - N: upper bound of range
    - num_threads: number of threads to use
    Returns: total sum of squares
    """
    chunk_size = N // num_threads
    results = [0] * num_threads
    threads = []

    # Create and start threads
    for i in range(num_threads):
        start_index = i * chunk_size + 1
        # Last thread takes the remainder
        end_index = (i + 1) * chunk_size + 1 if i != num_threads - 1 else N + 1
        thread = threading.Thread(
            target=compute_partial_squares,
            args=(start_index, end_index, results, i)
        )
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    # Combine partial results
    return sum(results)

# ==========================================
# Utility: Time Measurement
# ==========================================
def measure_time(func, *args):
    """
    Utility to measure execution time of a function.
    Returns: (elapsed_time, result)
    """
    start = time.time()
    result = func(*args)
    return time.time() - start, result

# ==========================================
# Main Execution
# ==========================================
if __name__ == "__main__":
    N = 5_000_000  # Example input size

    # Sequential execution
    t1, seq_result = measure_time(compute_sequential, N)

    # Parallel execution
    tp, par_result = measure_time(compute_parallel, N, 4)

    # Verify correctness
    assert seq_result == par_result

    # Performance metrics
    speedup = t1 / tp
    efficiency = speedup / 4

    # Output results
    print(f"Sequential Time: {t1:.4f}")
    print(f"Parallel Time: {tp:.4f}")
    print(f"Speedup: {speedup:.4f}")
    print(f"Efficiency: {efficiency:.4f}")