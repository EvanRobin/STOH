import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Parameters
L = 100       # Grid leangth
p = 0.6      # Starting Tree probability
f = 0.001      # Fire probability
g = 0.09      # Tree growth probability
steps = 1000   # Number of steps to simulate

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
def update(grid, g):
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
    
    catch_fire_spont = (grid == TREE) & (np.random.rand(L, L) < f)
    
    grow_tree = (grid == EMPTY) & (np.random.rand(L, L) < g)# Empty grows TREE
    
    # Fire dies to empty
    new_grid[grid == FIRE] = EMPTY
    new_grid[grow_tree] = TREE
    new_grid[catch_fire] = FIRE
    new_grid[catch_fire_spont] = FIRE

    return new_grid 

def count_fires(grid):
    unique, counts = np.unique(grid, return_counts=True)
    count_dict = dict(zip(unique, counts))
    return count_dict.get(0, 0)  # count_dict is {-1: empty, 0: fire, 1: tree}

def forest_fire(grid, g, max_steps):
    fire_time = 0

    for _ in range(max_steps):
        fires = count_fires(grid)
        if fires == 0:
            break
        fire_time += 1
        grid = update(grid, g)

    return fire_time



def eternal_flame(starting_g, max_g, step_g, max_steps):
    for i in np.arange(starting_g, max_g, step_g):
        grid = initialize_grid(L, p, f)
        if forest_fire(grid, i, max_steps) == max_steps:
            break
    return i

def eternal_flame_searching(starting_g, max_g, step_g, max_steps):
    for i in np.arange(starting_g, max_g, step_g):
        grid = initialize_grid(L, p, f)
        lifetime = forest_fire(grid, i, max_steps)
        print(f"g = {i:.4f}, fire lasted {lifetime} steps")
        if lifetime == max_steps:
            print(f"Forest maintains fire indefinitely for g ~= {i:.4f}")
            return i
    return None

best_g = eternal_flame_searching(0.001, 0.2, 0.001, 1000000)
print(f"Chosen g for sustained fire: {best_g}")

'''
g = 0.0100, fire lasted 1000 steps
Forest maintains fire indefinitely for g ~= 0.0100
Chosen g for sustained fire: 0.01

g = 0.0100, fire lasted 10000 steps
Forest maintains fire indefinitely for g ~= 0.0100
Chosen g for sustained fire: 0.01

to high start

g = 0.0010, fire lasted 67 steps
g = 0.0020, fire lasted 57698 steps
g = 0.0030, fire lasted 45 steps
g = 0.0040, fire lasted 1000000 steps
Forest maintains fire indefinitely for g ~= 0.0040
Chosen g for sustained fire: 0.004

tried many steps up to 1000000 all come to 4%

'''



