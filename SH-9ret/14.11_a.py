import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.ndimage import label
from matplotlib.colors import ListedColormap

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
def update(grid, f, g):
    L = grid.shape[0]
    new_grid = np.copy(grid)

    # Tree growth
    grow = (grid == EMPTY) & (np.random.rand(L, L) < g)
    new_grid[grow] = TREE

    # Lightning strikes
    lightning = (new_grid == TREE) & (np.random.rand(L, L) < f)
    new_grid[lightning] = FIRE

    # Spread fire from current FIRE trees
    burning = (new_grid == FIRE)
    neighbors = (
        np.roll(burning, 1, axis=0) | np.roll(burning, -1, axis=0) |
        np.roll(burning, 1, axis=1) | np.roll(burning, -1, axis=1)
    )
    fire_spread = (new_grid == TREE) & neighbors
    new_grid[fire_spread] = FIRE

    # Burned trees become empty
    new_grid[burning] = EMPTY

    return new_grid

# Cluster size analysis
def get_fire_cluster_sizes(grid):
    fire_mask = (grid == FIRE)
    structure = np.array([[0,1,0], [1,1,1], [0,1,0]])  # 4-neighbor connectivity
    labeled, num_features = label(fire_mask, structure=structure)
    sizes = np.bincount(labeled.ravel())[1:]  # Skip label 0 (background)
    return sizes

def animate_forest(grid, steps):
    cmap = ListedColormap(['white', 'red', 'green'])  # EMPTY, FIRE, TREE
    fig, ax = plt.subplots()
    im = ax.imshow(grid, cmap=cmap, vmin=-1, vmax=1)

    def update_frame(frame):
        nonlocal grid
        if frame >= steps + 1:
            ani.event_source.stop()
            return
        grid = update(grid, f, g)
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
animate_forest(grid, steps)





























'''
# Run simulation and collect N(s)
grid = initialize_grid(L, p)
cluster_stats = []

for step in range(steps):
    grid = update(grid, f, g)
    sizes = get_fire_cluster_sizes(grid)
    if len(sizes) > 0:
        cluster_stats.extend(sizes)

# Compute N(s)
from collections import Counter
Ns_counts = Counter(cluster_stats)

# Plot N(s) vs s in log-log
s_vals = np.array(list(Ns_counts.keys()))
Ns_vals = np.array(list(Ns_counts.values()))

plt.figure(figsize=(8,6))
plt.loglog(s_vals, Ns_vals, 'o', label=f"f={f}, g={g}")
plt.xlabel("Cluster size s")
plt.ylabel("N(s)")
plt.title("Cluster Size Distribution of Burned Trees")
plt.grid(True)
plt.legend()
plt.show()
'''