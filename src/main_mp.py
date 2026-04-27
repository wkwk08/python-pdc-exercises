import time
import threading
import multiprocessing as mp

# ==========================================
# Sequential Approach
# ==========================================
def compute_sequential(N: int) -> int:
    """Calculates the sum of squares sequentially."""
    return sum(i * i for i in range(1, N + 1))

# ==========================================
# Parallel Approach (Threads)
# ==========================================
def thread_worker(start: int, end: int, results: list, index: int):
    """Thread worker computes partial sum of squares."""
    results[index] = sum(i * i for i in range(start, end))

def compute_parallel(N: int, num_threads: int = 4) -> int:
    """Splits workload among threads and combines results."""
    chunk = N // num_threads
    results = [0] * num_threads
    threads = []

    for i in range(num_threads):
        start = i * chunk + 1
        end = (i + 1) * chunk + 1 if i != num_threads - 1 else N + 1
        t = threading.Thread(target=thread_worker, args=(start, end, results, i))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return sum(results)

# ==========================================
# Distributed Approach (Processes)
# ==========================================
def process_worker(start: int, end: int, queue: mp.Queue):
    """Process worker computes partial sum and sends to queue."""
    queue.put(sum(i * i for i in range(start, end)))

def compute_distributed(N: int, num_processes: int = 4) -> int:
    """Splits workload among processes and aggregates results."""
    chunk = N // num_processes
    queue = mp.Queue()
    processes = []

    for i in range(num_processes):
        start = i * chunk + 1
        end = (i + 1) * chunk + 1 if i != num_processes - 1 else N + 1
        p = mp.Process(target=process_worker, args=(start, end, queue))
        processes.append(p)
        p.start()

    total_sum = sum(queue.get() for _ in processes)

    for p in processes:
        p.join()

    return total_sum

# ==========================================
# Utility: Measure Time
# ==========================================
def measure_time(func, *args):
    """Utility to measure execution time of a function."""
    start = time.time()
    result = func(*args)
    return time.time() - start, result

# ==========================================
# Main Execution
# ==========================================
def main():
    try:
        N = int(input("Enter N: "))
    except ValueError:
        print("Invalid input. Please enter an integer.")
        return

    workers = 4  # number of threads/processes

    # Sequential
    t1, seq_result = measure_time(compute_sequential, N)

    # Parallel (Threads)
    tp, par_result = measure_time(compute_parallel, N, workers)

    # Distributed (Processes)
    td, dist_result = measure_time(compute_distributed, N, workers)

    # Sanity check
    assert seq_result == par_result == dist_result, "Mismatch in results!"

    # --- Performance Metrics ---
    # Speedup (S) = T1 / Tp
    # Efficiency (E) = S / p
    speedup_par = t1 / tp if tp > 0 else 0
    eff_par = speedup_par / workers
    speedup_dist = t1 / td if td > 0 else 0
    eff_dist = speedup_dist / workers

    # Output in expected format
    print(f"Sequential Time: {t1:.4f}")
    print(f"Parallel Time: {tp:.4f}")
    print(f"Distributed Time: {td:.4f}")
    print(f"\nSpeedup (Parallel): {speedup_par:.4f}")
    print(f"Efficiency (Parallel): {eff_par:.4f}")
    print(f"\nSpeedup (Distributed): {speedup_dist:.4f}")
    print(f"Efficiency (Distributed): {eff_dist:.4f}")

if __name__ == "__main__":
    main()