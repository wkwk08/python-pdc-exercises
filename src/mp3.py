import threading

balance = 0
lock = threading.Lock()

def deposit(amount, times):
    global balance
    for _ in range(times):
        with lock:  # prevents race condition
            balance += amount

if __name__ == "__main__":
    threads = []
    for _ in range(4):
        t = threading.Thread(target=deposit, args=(1, 1000))
        threads.append(t)
        t.start()
    for t in threads: t.join()
    print("Final Balance:", balance)