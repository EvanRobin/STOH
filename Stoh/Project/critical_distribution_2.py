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
f = 0.00001       # Fire probability
g = 0.1     # Tree growth probability
steps = 100000 # Number of steps to simulate

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
# Update step
def update_arossel_and_schwabl_model(grid, f, g):
    L = grid.shape[0]
    new_grid = np.copy(grid)

    # Step 1: Tree growth
    grow = (grid == EMPTY) & (np.random.rand(L, L) < g)
    new_grid[grow] = TREE

    # Step 2: Lightning strikes — ignite trees
    lightning = (new_grid == TREE) & (np.random.rand(L, L) < f)
    new_grid[lightning] = FIRE

    # Step 3: Instantaneous fire spread — flood fill from all FIRE cells
    fire_mask = (new_grid == FIRE)

    if np.any(fire_mask):
        # Trees that are potential to catch fire
        tree_mask = (new_grid == TREE)

        # Label all connected components of trees
        labeled_trees, num_features = label(tree_mask, structure=[[0,1,0],[1,1,1],[0,1,0]])

        # Find tree clusters that are adjacent to fire
        fire_neighbors = (
            np.roll(fire_mask, 1, axis=0) | np.roll(fire_mask, -1, axis=0) |
            np.roll(fire_mask, 1, axis=1) | np.roll(fire_mask, -1, axis=1)
        )
        ignite_labels = np.unique(labeled_trees[fire_neighbors & (labeled_trees > 0)])

        # Set all trees in those clusters on fire
        for lbl in ignite_labels:
            new_grid[labeled_trees == lbl] = FIRE

    # Step 4: Burned trees become empty
    new_grid[fire_mask] = EMPTY

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
    grid = update_arossel_and_schwabl_model(grid, g, f)
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

for i in range(20):#this can be 1 if not solving for problem d
    # Simulation
    all_cluster_sizes = []
    grid = initialize_grid(L, p, f)

    for step in range(steps):
        grid = update_arossel_and_schwabl_model(grid, g, f)
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
    print("for g and f", g, f)
    g*=1.1
    f*=1.1

'''
# Simulation
all_cluster_sizes = []
g=0.1
f=0.00001
L=100
steps=10**6
grid = initialize_grid(L, p, f)

for step in range(steps):
    grid = update_arossel_and_schwabl_model(grid, g, f)
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
print("for g and f", g, f)
'''
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
