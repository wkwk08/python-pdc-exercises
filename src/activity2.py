import time

# Number of processors/threads for this simulation
p = 2 

# Sequential
start = time.time()
total = sum(i*i for i in range(5_000_000))
end = time.time()
T1 = end - start

# Parallel (simple simulation)
start = time.time()
total = sum(i*i for i in range(5_000_000))
end = time.time()
Tp = end - start

# Print raw times
print("T1 (Sequential):", T1)
print("Tp (Parallel Simulation):", Tp)

# Compute Speedup and Efficiency
# Added a small check to prevent division by zero just in case
S = T1 / Tp if Tp > 0 else 0
E = S / p

# Print final computations
print(f"Speedup (S): {S:.4f}")
print(f"Efficiency (E): {E:.4f}")