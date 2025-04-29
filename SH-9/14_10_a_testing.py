import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Parameters
L = 10       # Grid leangth
p = 0.7      # Tree probability
f = 0.1      # Fire probability
g = 0.01      # Tree growth probability
steps = 200   # Number of steps to simulate

# States
EMPTY = 0
TREE = 1
FIRE = -1

# Initialize grid
def initialize_grid(L, p, f):
    grid = np.random.choice([EMPTY, TREE], size=(L, L), p=[1 - p, p])
    fire_start = (grid == TREE) & (np.random.rand(L, L) < f) #is this faster then for?
    grid[fire_start] = FIRE
    return grid






'''
  ╱|、
(•˕ •  7
 |、⁻〵ノ)
じしˍ,)ノ⠀
'''