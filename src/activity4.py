import threading

# Shared global variable
counter = 0
# Create a Lock object to prevent race conditions
lock = threading.Lock()

def increment():
    global counter
    for _ in range(100000):
        # Acquire the lock before modifying the shared variable
        lock.acquire()
        counter += 1
        # Release the lock so other threads can use it
        lock.release()

def test_synchronization():
    print("--- Synchronization Observation ---")
    threads = []
    
    # Start 2 threads, each incrementing 100,000 times
    for _ in range(2):
        t = threading.Thread(target=increment)
        threads.append(t)
        t.start()
        
    # Wait for all threads to finish
    for t in threads:
        t.join()
        
    # If successful, 2 threads * 100,000 increments = 200,000
    print("Final Counter:", counter)
    print("Expected: 200000")

if __name__ == '__main__':
    test_synchronization()