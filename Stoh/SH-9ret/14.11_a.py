import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import ListedColormap
from scipy.ndimage import label
from collections import defaultdict
import numpy as np
from scipy.stats import powerlaw
from scipy.optimize import curve_fit
import powerlaw


# Parameters
L = 100        # Grid size
p = 0.6        # Initial tree density
f = 0.001      # Lightning probability
g = 0.01       # Tree growth probability
steps = 1000   # Number of iterations

# States
TREE = 1
EMPTY = -1
FIRE = 0

# Initialize grid
def initialize_grid(L, p, f):
    grid = np.random.choice([EMPTY, TREE], size=(L, L), p=[1 - p, p])
    return grid

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

# Cluster size analysis
def get_fire_cluster_sizes(grid):
    fire_mask = (grid == FIRE)
    structure = np.array([[0,1,0], [1,1,1], [0,1,0]])  # 4-neighbor connectivity
    labeled, num_features = label(fire_mask, structure=structure)
    sizes = np.bincount(labeled.ravel())[1:]  # Skip label 0 (background)
    return sizes

def animate_forest(grid, steps):
    cmap = ListedColormap(['blue', 'red', 'green'])  # EMPTY, FIRE, TREE
    fig, ax = plt.subplots()
    im = ax.imshow(grid, cmap=cmap, vmin=-1, vmax=1)

    def update_frame(frame):
        nonlocal grid
        if frame >= steps + 1:
            ani.event_source.stop()
            return
        grid = update_arossel_and_schwabl_model(grid, f, g)
        im.set_data(grid)
        ax.set_title(f"Step {frame}")
        return [im]

    ani = animation.FuncAnimation(
        fig, update_frame, interval=100, frames=steps + 1,
        blit=False, cache_frame_data=False
    )
    plt.show()

    ani = animation.FuncAnimation(fig, update_frame, interval=1000, blit=False) #interval 1 for 1 miliseconds and blit makes it to only animate when something changes if on TRUE
    plt.show()

# Run simulation
grid = initialize_grid(L, p, f)
'''
animate_forest(grid, steps)
'''

#copied from 14_10_cnew_testing.py

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
    grid = update_arossel_and_schwabl_model(grid, f, g)

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