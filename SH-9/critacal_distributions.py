import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import label
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.stats import powerlaw
from scipy.optimize import curve_fit
import powerlaw

# Parameters
L = 40       # Grid length
p = 0.6      # Starting tree probability
f = 0.1      # Fire probability
g = 0.082     # Tree growth probability
steps = 10000  # Number of steps to simulate

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
    L = grid.shape[0]
    neighbors = [
        np.roll(grid, 1, axis=0),
        np.roll(grid, -1, axis=0),
        np.roll(grid, 1, axis=1),
        np.roll(grid, -1, axis=1),
    ]
    fire_neighbors = sum((n == FIRE) for n in neighbors)
    catch_fire = (grid == TREE) & (fire_neighbors > 0)
    grow_tree = (grid == EMPTY) & (np.random.rand(L, L) < g)

    new_grid[grid == FIRE] = EMPTY
    new_grid[grow_tree] = TREE
    new_grid[catch_fire] = FIRE
    return new_grid

# Analyze fire clusters in current grid
from collections import defaultdict

from collections import defaultdict

def analyze_fire_clusters(grid):
    fire_mask = (grid == FIRE)
    labeled_array, num_features = label(fire_mask)
    
    cluster_size_counts = defaultdict(int)  # key: cluster size, value: how many of that size

    for cluster_id in range(1, num_features + 1): #num_features are the number of clusters
        coords = np.argwhere(labeled_array == cluster_id)
        size = len(coords)
        cluster_size_counts[size] += 1  # count how many clusters of this size

    return cluster_size_counts, num_features

# --- Collect cluster sizes over multiple steps ---
all_cluster_sizes = []

grid = initialize_grid(L, p, f)

for step in range(steps):
    grid = update(grid, g)
    cluster_counts, _ = analyze_fire_clusters(grid)

    for size, count in cluster_counts.items():
        all_cluster_sizes.extend([size] * count)  # Add 'count' copies of 'size'

#Plot N(s) ands s
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np

size_counter = Counter(all_cluster_sizes)

sizes = np.array(list(size_counter.keys()))
Ns = np.array(list(size_counter.values()))

# Sort by size for smooth plotting
sorted_indices = np.argsort(sizes)
sizes = sizes[sorted_indices]
Ns = Ns[sorted_indices]

fit = powerlaw.Fit(all_cluster_sizes, discrete=True)
print(f"Estimated power law exponent (alpha): {fit.alpha}")
print(f"xmin (start of power law behavior): {fit.xmin}")

# Plot with fit
fig = fit.plot_pdf(color='blue', marker='o', linestyle='None', label='Data') 
fit.power_law.plot_pdf(color='red', linestyle='--', ax=fig, label='Power law fit')  # optional line for fit
plt.xlabel("Cluster size (s)")
plt.ylabel("P(s)")
plt.title("Power-law fit to cluster size distribution")
plt.legend()
plt.grid(True, which="both", ls="--", linewidth=0.5)
plt.show()
