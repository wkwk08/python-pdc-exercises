import threading, multiprocessing as mp

def thread_row_sum(rows, results, idx):
    """Thread worker computes row sums for a chunk of rows."""
    results[idx] = [sum(row) for row in rows]

def process_worker(matrix_chunk, queue):
    """Process worker uses threads inside each process."""
    num_threads = 2
    chunk_size = len(matrix_chunk) // num_threads
    results = [None] * num_threads
    threads = []
    for i in range(num_threads):
        start = i * chunk_size
        end = (i+1) * chunk_size if i != num_threads-1 else len(matrix_chunk)
        t = threading.Thread(target=thread_row_sum, args=(matrix_chunk[start:end], results, i))
        threads.append(t)
        t.start()
    for t in threads: t.join()
    combined = [row for part in results for row in part]
    queue.put(combined)

def hybrid_matrix_sum(matrix, num_processes=2):
    """Hybrid computation: processes split matrix, threads compute row sums."""
    chunk_size = len(matrix) // num_processes
    queue = mp.Queue()
    processes = []
    for i in range(num_processes):
        start = i * chunk_size
        end = (i+1) * chunk_size if i != num_processes-1 else len(matrix)
        p = mp.Process(target=process_worker, args=(matrix[start:end], queue))
        processes.append(p)
        p.start()
    results = [row for _ in processes for row in queue.get()]
    for p in processes: p.join()
    return results

if __name__ == "__main__":
    # A 6x5 matrix with varied values
    matrix = [
        [1, 2, 3, 4, 5],      # sum = 15
        [10, 20, 30, 40, 50], # sum = 150
        [2, 4, 6, 8, 10],     # sum = 30
        [3, 6, 9, 12, 15],    # sum = 45
        [5, 5, 5, 5, 5],      # sum = 25
        [7, 14, 21, 28, 35]   # sum = 105
    ]
    print("Row sums:", hybrid_matrix_sum(matrix))