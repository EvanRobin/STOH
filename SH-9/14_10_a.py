import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Parameters
L = 100        # Grid size
p = 0.75        # Initial tree probability
f = 0.001      # Initial fire probability
g = 0.0001       # Tree growth probability
steps = 200    # Number of steps to simulate

# States
EMPTY = 0
TREE = 1
FIRE = 2

# Initialize grid
def initialize_grid(L, p, f):
    grid = np.random.choice([EMPTY, TREE], size=(L, L), p=[1 - p, p])
    fire_mask = (grid == TREE) & (np.random.rand(L, L) < f)
    grid[fire_mask] = FIRE
    return grid

# Update step
def update(grid):
    new_grid = np.copy(grid)
    L = grid.shape[0]
    
    # Neighbor shift N S E W
    neighbors = [
        np.roll(grid, 1, axis=0),
        np.roll(grid, -1, axis=0),
        np.roll(grid, 1, axis=1),
        np.roll(grid, -1, axis=1),
    ]
    # Trees that catch fire if any neighbor is on fire
    fire_neighbors = sum((n == FIRE) for n in neighbors)
    catch_fire = (grid == TREE) & (fire_neighbors > 0)
    
    # Empty grows tree
    grow_tree = (grid == EMPTY) & (np.random.rand(L, L) < g)
    
    # Fire dies to empty
    new_grid[grid == FIRE] = EMPTY
    new_grid[grow_tree] = TREE
    new_grid[catch_fire] = FIRE

    return new_grid

# Visualization setup
def animate_forest(grid, steps):
    cmap = plt.cm.get_cmap('brg', 3)
    fig, ax = plt.subplots()
    im = ax.imshow(grid, cmap=cmap, vmin=0, vmax=2)

    def update_frame(frame):
        nonlocal grid
        grid = update(grid)
        im.set_data(grid)
        ax.set_title(f"Step {frame}")
        return [im]

    ani = animation.FuncAnimation(fig, update_frame, frames=steps, interval=100, blit=True)
    plt.show()

# Run simulation
grid = initialize_grid(L, p, f)
animate_forest(grid, steps)