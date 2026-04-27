import time
import random

def test_memory_hierarchy():
    print("--- Memory Hierarchy Observation ---")
    
    # Generating a massive list of 10 million numbers
    data = list(range(10_000_000))
    
    # ---------------------------------------------------------
    # 1. Sequential access (cache-friendly)
    # ---------------------------------------------------------
    start = time.time()
    for i in data:
        x = i * 2
    end = time.time()
    seq_time = end - start
    print(f"Sequential access: {seq_time:.4f} seconds")
    
    # ---------------------------------------------------------
    # 2. Random access (cache-unfriendly)
    # ---------------------------------------------------------
    start = time.time()
    for _ in range(10_000_000):
        # Grabbing a random index instead of going in order
        x = data[random.randint(0, 9999999)]
    end = time.time()
    rand_time = end - start
    print(f"Random access:     {rand_time:.4f} seconds")

if __name__ == '__main__':
    test_memory_hierarchy()