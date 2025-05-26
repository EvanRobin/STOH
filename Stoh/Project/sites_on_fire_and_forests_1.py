import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.stats import powerlaw
from scipy.optimize import curve_fit
import powerlaw

# Parameters
L = 40       # Grid leangth
p = 0.6      # Starting Tree probability
f = 0.1      # Fire probability
g = 0.082      # Tree growth probability
steps = 10**4   # Number of steps to simulate

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
    
    grow_tree = (grid == EMPTY) & (np.random.rand(L, L) < g)# EMPTY grows TREE
    
    # Fire dies to empty
    new_grid[grid == FIRE] = EMPTY
    new_grid[grow_tree] = TREE
    new_grid[catch_fire] = FIRE

    return new_grid




def count_fires(grid):
    unique, counts = np.unique(grid, return_counts=True)
    count_dict = dict(zip(unique, counts))
    return count_dict.get(0, 0)  # count_dict is {-1: empty, 0: fire, 1: tree}

def count_trees(grid):
    unique, counts = np.unique(grid, return_counts=True)
    count_dict = dict(zip(unique, counts))
    return count_dict.get(1, 1)  # count_dict is {-1: empty, 0: fire, 1: tree}


def sf_and_st(grid, g, steps):
    sf_list = []
    st_list = []

    for _ in range(steps):
        sf_list.append(count_fires(grid))
        st_list.append(count_trees(grid))
        grid = update(grid, g)

    return np.array(sf_list), np.array(st_list) 

# Run the simulation
grid = initialize_grid(L, p, f)
sf, st = sf_and_st(grid, g, steps)

# we dont want zeros
sf_nonzero = sf[sf > 0]
st_nonzero = st[st > 0]

# Plot histogram of number of sites on fire (sf)
plt.figure(figsize=(8, 6))
plt.hist(sf_nonzero, bins=30, density=True, alpha=0.7, color='orangered', edgecolor='black')
plt.title("Distribution of Sites on Fire")
plt.xlabel("Number of Sites on Fire")
plt.ylabel("Probability Density")
plt.grid(True)
plt.tight_layout()
plt.show()
plt.figure(figsize=(8, 6))
plt.hist(st_nonzero, bins=30, density=True, alpha=0.7, color='green', edgecolor='black')
plt.title("Distribution of Sites on with Trees")
plt.xlabel("Number of Sites on Fire")
plt.ylabel("Probability Density")
plt.grid(True)
plt.tight_layout()
