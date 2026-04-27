import threading
from multiprocessing import Process, Queue

# ---------------------------------------------------------
# Worker Functions
# ---------------------------------------------------------
def thread_task(thread_id):
    """Task executed by a thread (Parallel computing)."""
    print(f"Thread {thread_id} running")


def process_task(q, process_id):
    """Task executed by a process (Distributed-style computing)."""
    q.put(f"Process {process_id} running")


# ---------------------------------------------------------
# Execution Functions
# ---------------------------------------------------------
def run_threads():
    """Demonstrates thread-based parallel execution."""
    print("--- Starting Threads ---")
    threads = []
    
    # Create and start 2 threads
    for i in range(2):
        t = threading.Thread(target=thread_task, args=(i+1,))
        threads.append(t)
        t.start()
        
    # Wait for all threads to complete
    for t in threads:
        t.join()


def run_processes():
    """Demonstrates process-based distributed-style execution."""
    print("\n--- Starting Processes ---")
    q = Queue()
    processes = []
    
    # Create and start 2 processes
    for i in range(2):
        p = Process(target=process_task, args=(q, i+1))
        processes.append(p)
        p.start()
        
    # Retrieve and print messages from the queue
    for _ in processes:
        print(q.get())
        
    # Wait for all processes to complete
    for p in processes:
        p.join()


# ---------------------------------------------------------
# Main Block
# ---------------------------------------------------------
if __name__ == "__main__":
    run_threads()
    run_processes()