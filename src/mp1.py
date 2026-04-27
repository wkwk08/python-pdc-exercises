import threading

def compute_partial_sum(array, start_index, end_index, results, thread_id):
    """
    Thread worker: computes partial sum of a slice of the array.
    """
    results[thread_id] = sum(array[start_index:end_index])

def compute_parallel_sum(array, num_threads=4):
    """
    Divide array into chunks, compute sum in parallel using threads.
    """
    chunk_size = len(array) // num_threads  # size of each chunk
    results = [0] * num_threads             # store partial sums
    threads = []                            # keep track of threads

    # Create and start threads
    for i in range(num_threads):
        start_index = i * chunk_size
        end_index = (i + 1) * chunk_size if i != num_threads - 1 else len(array)
        thread = threading.Thread(
            target=compute_partial_sum,
            args=(array, start_index, end_index, results, i)
        )
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    # Combine partial results
    return sum(results)

if __name__ == "__main__":
    # Example input array: integers from 1 to 50,000
    data_array = list(range(1, 50001))
    total_sum = compute_parallel_sum(data_array)
    print("Total Sum:", total_sum)