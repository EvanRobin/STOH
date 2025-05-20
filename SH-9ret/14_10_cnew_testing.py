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
def analyze_fire_clusters(grid):
    fire_mask = (grid == FIRE)
    labeled_array, num_features = label(fire_mask)
    cluster_sizes = []
    cluster_radii = []

    for cluster_id in range(1, num_features + 1):
        coords = np.argwhere(labeled_array == cluster_id)
        size = len(coords)
        centroid = coords.mean(axis=0)
        rms_radius = np.sqrt(np.mean(np.sum((coords - centroid) ** 2, axis=1)))

        cluster_sizes.append(size)
        cluster_radii.append(rms_radius)

    return cluster_sizes, cluster_radii

# Main simulation loop to accumulate statistics
cluster_size_counts = defaultdict(int)
cluster_radius_sums = defaultdict(float)

grid = initialize_grid(L, p, f)
for _ in range(steps):
    sizes, radii = analyze_fire_clusters(grid)
    for s, r in zip(sizes, radii):
        cluster_size_counts[s] += 1
        cluster_radius_sums[s] += r
    grid = update(grid, g)

# Compute averages
cluster_sizes = sorted(cluster_size_counts.keys())
mean_counts = [cluster_size_counts[s] / steps for s in cluster_sizes]
mean_radii = [cluster_radius_sums[s] / cluster_size_counts[s] for s in cluster_sizes]

# Save data for external analysis (optional)
'''
np.savetxt("cluster_stats.txt", np.column_stack([cluster_sizes, mean_counts, mean_radii]),
           header="cluster_size mean_count mean_radius", comments='')
'''
import powerlaw

# Convert data to raw sample with weights (reconstruct individual sizes)
raw_cluster_sizes = []
for size, count in zip(cluster_sizes, cluster_size_counts.values()):
    raw_cluster_sizes.extend([size] * count)

# Use powerlaw package to fit the raw cluster sizes
fit = powerlaw.Fit(raw_cluster_sizes, discrete=True)

# Get alpha (the exponent), and x_min (cutoff where power law starts)
alpha = fit.alpha
xmin = fit.xmin
print(f"Fitted power-law exponent alpha: {alpha:.3f}")
print(f"Fitted xmin: {xmin}") 

plt.figure(figsize=(12, 5))

# Plot the empirical PDF (Probability Density Function)
fit.plot_pdf(label="Simulation Data", color='blue', marker='o')

# Plot the fitted power-law model
fit.power_law.plot_pdf(label=f"Power-law fit\nα = {fit.alpha:.2f}", color='red', linestyle='--')

# Formatting
plt.xscale('log')
plt.yscale('log')
plt.xlabel("Cluster Size (s)")
plt.ylabel("P(s)")
plt.title("PDF of Cluster Sizes with Power-law Fit")
plt.grid(True, which='both', ls=':')
plt.legend()
plt.tight_layout()
plt.show()


'''
2.754
4.427
3.366
3.252
Fitted power-law exponent alpha: 3.089
Fitted power-law exponent alpha: 5.140
Fitted power-law exponent alpha: 2.986

Fitted power-law exponent alpha: 5.351
'''