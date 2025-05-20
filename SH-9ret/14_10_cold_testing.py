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
'''
# Plot histogram of number of sites on fire (sf)
plt.figure(figsize=(8, 6))
plt.hist(sf_nonzero, bins=30, density=True, alpha=0.7, color='orangered', edgecolor='black')
plt.title("Distribution of Sites on Fire")
plt.xlabel("Number of Sites on Fire")
plt.ylabel("Probability Density")
plt.grid(True)
plt.tight_layout()
plt.show()
'''

'''

import numpy as np

# Compute histogram (PDF)
counts, bin_edges = np.histogram(sf_nonzero, bins=30, density=True)
bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

# Filter out zero probabilities for cleaner data
mask = counts > 0
bin_centers = bin_centers[mask]
counts = counts[mask]

# Save to txt file with two columns: "fire_size probability"
output_data = np.column_stack((bin_centers, counts))
np.savetxt("fire_size_distribution.txt", output_data, header="fire_size probability", comments='')

print("Data saved to fire_size_distribution.txt")


gnuplot;

# Load data and plot
plot "fire_size_distribution.txt" using 1:2 with points pt 7 title "Data"

# Fit power-law: y = a*x^(-b)
f(x) = a * x**(-b)
fit f(x) "fire_size_distribution.txt" using 1:2 via a,b

# Plot fit and data
plot "fire_size_distribution.txt" using 1:2 with points pt 7 title "Data", \
     f(x) with lines lw 2 title sprintf("Fit: b=%.3f", b)
'''

'''
# Plot histogram of number of sites with trees (st)
plt.figure(figsize=(8, 6))
plt.hist(st_nonzero, bins=30, density=True, alpha=0.7, color='green', edgecolor='black')
plt.title("Distribution of Sites with trees")
plt.xlabel("Number of Sites with trees")
plt.ylabel("Probability Density")
plt.grid(True)
plt.tight_layout()
plt.show()
'''

# Assuming st and sf are numpy arrays of the same length
correlation = np.corrcoef(st, sf)[0, 1]

print(f"Pearson correlation coefficient between number of trees and fires: {correlation:.4f}")

plt.scatter(st, sf, alpha=0.5, s=10)
plt.xlabel('Number of Trees (st)')
plt.ylabel('Number of Fires (sf)')
plt.title(f'Correlation between Trees and Fires: {correlation:.2f}')
plt.grid(True)
plt.show()


