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

    ani = animation.FuncAnimation(fig, update_frame, interval=1000, blit=True) #interval 1 for 1 miliseconds and blit makes it to only animate when something changes if on TRUE
    plt.show()


# Run simulation
grid = initialize_grid(L, p, f)
'''
animate_forest(grid, steps)
'''

def show_forest_frame(grid):
    cmap = plt.colormaps['brg'].resampled(3)
    fig, ax = plt.subplots()
    im = ax.imshow(grid, cmap=cmap, vmin=-1, vmax=1)
    ax.set_title("Forest grid")
    plt.show()




# Or after a few updates:
for _ in range(100):
    grid = update_arossel_and_schwabl_model(grid, f, g)


show_forest_frame(grid)  # Show the state after 10 steps
