import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Parameters
L = 100       # Grid leangth
p = 0.8      # Tree probability
f = 0.1      # Fire probability
g = 0.1      # Tree growth probability
steps = 200   # Number of steps to simulate

# States
TREE = 1
EMPTY = -1
FIRE = 0

# Initialize grid
def initialize_grid(L, p, f):
    grid = np.random.choice([EMPTY, TREE], size=(L, L), p=[1 - p, p]) #filling the grid of size L L with EMPTy OR TREE
    fire_start = (grid == TREE) & (np.random.rand(L, L) < f) #is this faster then for?
    grid[fire_start] = FIRE #TREE is on FIRE
    return grid

# New step
def update(grid):
    new_grid = np.copy(grid)
    L = grid.shape[0]
    
    # Neighbor shift N S E W
    neighbors = [
        np.roll(grid, 1, axis=0), #Moves Up
        np.roll(grid, -1, axis=0), #Down
        np.roll(grid, 1, axis=1), #Lef
        np.roll(grid, -1, axis=1), #Right
    ]


    fire_neighbors = sum((n == FIRE) for n in neighbors)
    catch_fire = (grid == TREE) & (fire_neighbors > 0) #A tree catches fire if any neighbor is on fire.
    
    grow_tree = (grid == EMPTY) & (np.random.rand(L, L) < g)# Empty grows TREE
    
    # Fire dies to empty
    new_grid[grid == FIRE] = EMPTY
    new_grid[grow_tree] = TREE
    new_grid[catch_fire] = FIRE

    return new_grid 
'''
# Animation
def animate_forest(grid, steps):
    cmap = plt.colormaps['brg'].resampled(3) #Gets the color map named 'brg' (blue-red-green), the resampled part solves some error
    fig, ax = plt.subplots()
    im = ax.imshow(grid, cmap=cmap, vmin=-1, vmax=1) #that values go from -1 to 1

    def update_frame(frame):
        nonlocal grid #this makes it all run once per frame
        if frame >= steps + 1:
            ani.event_source.stop()  # Stops the loop
            return
        grid = update(grid)
        im.set_data(grid)
        ax.set_title(f"Step {frame}")
        return [im]

    ani = animation.FuncAnimation(fig, update_frame, interval=1000, blit=False) #interval 1 for 1 miliseconds and blit makes it to only animate when something changes if on TRUE
    plt.show()

# Run simulation
grid = initialize_grid(L, p, f)
animate_forest(grid, steps)
'''
'''
  ╱|、
(•˕ •  7
 |、⁻〵ノ)
じしˍ,)ノ
'''

def show_forest_frame(grid):
    cmap = plt.colormaps['brg'].resampled(3)
    fig, ax = plt.subplots()
    im = ax.imshow(grid, cmap=cmap, vmin=-1, vmax=1)
    ax.set_title("Forest grid")
    plt.show()

grid = initialize_grid(L, p, f)
show_forest_frame(grid)  # Show the initial state

# Or after a few updates:
for _ in range(100):
    grid = update(grid)


show_forest_frame(grid)  # Show the state after 10 steps