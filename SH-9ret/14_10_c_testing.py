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
g = 0.09      # Tree growth probability
steps = 10**3   # Number of steps to simulate

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

def estimate_alpha_maximum_Likeleyhood_method(data, xmin=1):
    data = np.array(data)
    data = data[data >= xmin]
    n = len(data)
    if n == 0:
        return np.nan, data
    alpha = 1 + n / np.sum(np.log(data / (xmin - 0.5)))  # MLE formula
    return alpha, data


xmin = 10  # seems that 10 is best
xmin = 10


alpha_sf, data_sf = estimate_alpha_maximum_Likeleyhood_method(sf_nonzero, xmin)


counts, bin_edges = np.histogram(data_sf, bins=np.logspace(np.log10(xmin), np.log10(data_sf.max()), 30), density=True)
bin_centers = np.sqrt(bin_edges[:-1] * bin_edges[1:])  # geometric mean for log binning

plt.figure(figsize=(8, 6))
plt.plot(bin_centers, counts, 'o', label='Empirical PDF (sf)', markersize=5)

#power-law fit
x_fit = np.linspace(xmin, data_sf.max(), 100)
y_fit = (alpha_sf - 1) / (xmin - 0.5) * (x_fit / (xmin - 0.5)) ** (-alpha_sf)
plt.plot(x_fit, y_fit, '--r', label=f'Power-law fit (α = {alpha_sf:.2f})')

plt.xscale('log')
plt.yscale('log')
plt.xlabel('Number of fire sites (sf)')
plt.ylabel('Probability density')
plt.title('Empirical PDF vs MLE Power-law Fit')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()