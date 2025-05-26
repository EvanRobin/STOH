import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import label
from collections import defaultdict, Counter
from scipy import stats as S
from collections import Counter
from scipy.stats import linregress

# Parameters
L = 40        # Grid length
p = 0.6       # Starting tree probability
f = 0.1       # Fire probability
g = 0.082     # Tree growth probability
steps = 100 # Number of steps to simulate

# States
TREE = 1
EMPTY = -1
FIRE = 0

# Initialize grid
def initialize_grid(L, p, f):
    grid = np.random.choice([EMPTY, TREE], size=(L, L), p=[1 - p, p])
    fire_start = (grid == TREE) & (np.random.rand(L, L) < f)
    grid[fire_start] = FIRE
    return grid

# Update grid
def update(grid, g):
    new_grid = np.copy(grid)
    neighbors = [
        np.roll(grid, 1, axis=0),   # Up
        np.roll(grid, -1, axis=0),  # Down
        np.roll(grid, 1, axis=1),   # Left
        np.roll(grid, -1, axis=1),  # Right
    ]
    fire_neighbors = sum((n == FIRE) for n in neighbors)
    catch_fire = (grid == TREE) & (fire_neighbors > 0)
    grow_tree = (grid == EMPTY) & (np.random.rand(*grid.shape) < g)

    new_grid[grid == FIRE] = EMPTY
    new_grid[grow_tree] = TREE
    new_grid[catch_fire] = FIRE
    return new_grid

# Analyze fire clusters
def analyze_fire_clusters(grid):
    fire_mask = (grid == FIRE)
    labeled_array, num_features = label(fire_mask)
    cluster_size_counts = defaultdict(int)
    for cluster_id in range(1, num_features + 1):
        size = np.sum(labeled_array == cluster_id)
        cluster_size_counts[size] += 1
    return cluster_size_counts

# Simulation loop
all_cluster_sizes = []
grid = initialize_grid(L, p, f)

for step in range(steps):
    grid = update(grid, g)
    cluster_counts = analyze_fire_clusters(grid)
    for size, count in cluster_counts.items():
        all_cluster_sizes.extend([size] * count)


'''
# Save to text file for Gnuplot
output_file = "cluster_data.txt"
with open(output_file, "w") as file:
    file.write("# ClusterSize(s)\tCount(N(s))\n")
    for s, n in zip(sizes, Ns):
        file.write(f"{s}\t{n}\n")
'''
from collections import Counter

for i in range(10):#this can be 1 if not solving for problem d
    # Simulation
    all_cluster_sizes = []
    grid = initialize_grid(L, p, f)

    for step in range(steps):
        grid = update(grid, g)
        cluster_counts = analyze_fire_clusters(grid)
        for size, count in cluster_counts.items():
            all_cluster_sizes.extend([size] * count)

    # Count frequencies
    from collections import Counter
    size_counter = Counter(all_cluster_sizes)
    sizes = np.array(sorted(size_counter))
    Ns = np.array([size_counter[s] for s in sizes])

    # Log-log fit
    log_sizes = np.log10(sizes)
    log_Ns = np.log10(Ns)

    slope, intercept, r_value, p_value, std_err = linregress(log_sizes, log_Ns)
    alpha = -slope
    A = 10**intercept

    print(f"Estimated alpha: {alpha:.4f}")
    print(f"Estimated A: {A:.4e}")

# Plotting
plt.figure(figsize=(8, 6))
plt.plot(log_sizes, log_Ns, 'o', label='Data')
plt.plot(log_sizes, slope * log_sizes + intercept, 'r--', label=f'Fit: N(s) = {A:.2e} * s^(-{alpha:.2f})')
plt.xlabel("log10(s)")
plt.ylabel("log10(N(s))")
plt.title("Power-Law Fit to N(s) ∼ s^(-α)")
plt.grid(True, which="both", ls="--", linewidth=0.5)
plt.legend()
plt.tight_layout()
plt.show()


'''
Estimated alpha: 5.9379
Estimated A: 9.8195e+05
Estimated alpha: 6.2045
Estimated A: 1.1539e+06
Estimated alpha: 6.7826
Estimated A: 9.0040e+05
Estimated alpha: 6.7849
Estimated A: 1.4490e+06
Estimated alpha: 6.6719
Estimated A: 1.0777e+06
Estimated alpha: 6.1580
Estimated A: 3.6630e+05
Estimated alpha: 6.4582
Estimated A: 1.0759e+06
Estimated alpha: 6.2822
Estimated A: 8.4616e+05
Estimated alpha: 6.6699
Estimated A: 8.1972e+05
Estimated alpha: 7.4623
Estimated A: 1.3778e+06
10^6 steps
'''

'''
Estimated alpha: 6.3691
Estimated A: 3.6500e+05
Estimated alpha: 8.8835
Estimated A: 7.6631e+05
Estimated alpha: 5.8690
Estimated A: 3.0778e+05
Estimated alpha: 6.0638
Estimated A: 3.3429e+05
Estimated alpha: 5.9861
Estimated A: 3.1633e+05
Estimated alpha: 6.5003
Estimated A: 2.6160e+05
Estimated alpha: 5.7419
Estimated A: 3.1029e+05
Estimated alpha: 5.7092
Estimated A: 1.6439e+05
Estimated alpha: 6.7684
Estimated A: 2.5492e+05
Estimated alpha: 7.2136
Estimated A: 2.4147e+05

this was achived for 10^5 steps
'''

'''
Estimated alpha: 4.6547
Estimated A: 9.6938e+04
Estimated alpha: 6.5193
Estimated A: 9.3843e+04
Estimated alpha: 5.8451
Estimated A: 5.2256e+04
Estimated alpha: 5.1044
Estimated A: 7.3760e+04
Estimated alpha: 5.4701
Estimated A: 5.5702e+04
Estimated alpha: 5.5008
Estimated A: 6.6372e+04
Estimated alpha: 4.9367
Estimated A: 5.3059e+04
Estimated alpha: 5.1499
Estimated A: 1.0958e+05
Estimated alpha: 5.7206
Estimated A: 4.9112e+04
Estimated alpha: 4.9853
Estimated A: 6.9503e+04

this was achived for 10^4 steps
'''

'''
Estimated alpha: 4.6952
Estimated A: 1.5560e+04
Estimated alpha: 4.2834
Estimated A: 2.0434e+04
Estimated alpha: 5.1805
Estimated A: 2.0171e+04
Estimated alpha: 4.3177
Estimated A: 2.9112e+04
Estimated alpha: 4.7781
Estimated A: 2.5700e+04
Estimated alpha: 5.0365
Estimated A: 2.0531e+04
Estimated alpha: 4.3075
Estimated A: 2.2722e+04
Estimated alpha: 4.0234
Estimated A: 1.9746e+04
Estimated alpha: 4.3556
Estimated A: 3.3423e+04
Estimated alpha: 4.5319
Estimated A: 1.5797e+04
3
'''