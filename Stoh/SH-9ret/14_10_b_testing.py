import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Parameters
L = 40       # Grid leangth
p = 0.6      # Starting Tree probability
f = 0.1      # Fire probability
g = 0.09      # Tree growth probability
steps = 10**6   # Number of steps to simulate

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

'''
print(eternal_flame(0.075, 0.1, 0.005, 50000000)) #took 2 hours never again
'''

'''
so the first step was from 0 to 0.2 with step of 0.0001 with max time of 10000
result was 0.045700000000000005
second was eternal_flame(0.0, 0.05, 0.00001, 10000)
result was 0.041030000000000004
third print(eternal_flame(0.039, 0.05, 0.00001, 100000))
showed 0.05000000000000337
conclusion is time should be longer and steps smaller
forth eternal_flame(0.05, 0.5, 0.01, 100000)
0.07 i should now steadily increase stepps and time
I increased time instead again with eternal_flame(0.05, 0.8, 0.01, 1000000) got 0.08
so I added another 0 to time with eternal_flame(0.06, 0.1, 0.01, 10000000)
gaining 0.07999999999999999 this leads me to beileve that 1,000,000 is a completely fine if it gets the same value as 10,000,000
got 0.07 with 1,000,000 back to the drawing board
we shall try 5,000,000 with eternal_flame(0.07, 0.1, 0.001, 5000000)
0.07200000000000001

with eternal_flame(0.075, 0.1, 0.005, 50 000 000) the result is 0.085 

i shall round it to 9% for a L = 40

'''


'''
grid = initialize_grid(L, p, f)
print(forest_fire(grid, 0.3, 10000))
'''
'''
# Animation cant take it

# Simulation
grid = initialize_grid(L, p, f)
for _ in range(steps):
    grid = update(grid, g)

# Plot final state
cmap = plt.colormaps['brg'].resampled(3)
plt.imshow(grid, cmap=cmap, vmin=-1, vmax=1)
plt.title(f"Final Forest State after {steps:,} Steps")
plt.axis('off')
plt.show()
'''
hl=10
for i  in range(hl):
    print(eternal_flame(0.078, 0.1, 0.001, 10**6)) 

