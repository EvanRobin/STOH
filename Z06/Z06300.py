import numpy as np
import matplotlib.pyplot as plt
import math
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
 
# Parameters
 
x = 0.0  # starting point
y = 0.0
z = 0.0
sigma = 2.0  # width

n_steps = 5000
frame_skip = 50  # animation speed
sigma = 2.0

# P(x, y, z) =  |3, 0, 0> from http://employees.csbsju.edu/hjakubowski/classes/ch123/Quantum/EquationsOribtalsH.htm also a0 = 1
def prob(x, y, z):
    r = math.sqrt(x**2 + y**2 + z**2)
    return ((27 - 18*r + (2*r**2))**2)*np.exp(-2*r/3)
 
# Function to evaluate: z
def f(x, y, z):
    return z
 
x_vals = []
y_vals = []
z_vals = []
r_vals = []
 
for _ in range(n_steps):
    x_new = x + np.random.normal(0, sigma)
    y_new = y + np.random.normal(0, sigma)
    z_new = z + np.random.normal(0, sigma)
     
    acceptance_ratio = prob(x_new, y_new, z_new) / prob(x, y, z)
     
    if np.random.rand() < acceptance_ratio:
        x = x_new
        y = y_new
        z = z_new
 
    y_vals.append(y)
    x_vals.append(x)
    z_vals.append(f(x, y, z))
    r_vals.append(math.sqrt(x**2 + y**2 + z**2))
 
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')
sc = ax.scatter([], [], [], s=2, alpha=0.6)

ax.set_xlim(-30, 30)
ax.set_ylim(-30, 30)
ax.set_zlim(-30, 30)
ax.set_title("Hydrogen Atom (3s Orbital) - Metropolis Sampling")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.view_init(azim=60, elev=20)

# Initialization
def init():
    sc._offsets3d = ([], [], [])
    return sc,

# Animation update function
def update(frame):
    end = frame * frame_skip
    xs = x_vals[:end]
    ys = y_vals[:end]
    zs = z_vals[:end]
    sc._offsets3d = (xs, ys, zs)
    ax.set_title(f"Hydrogen Atom Sampling\nStep {end}")
    return sc,

# Create animation
frames = n_steps // frame_skip
ani = animation.FuncAnimation(fig, update, frames=frames, init_func=init, interval=100, blit=False)

plt.show()

# Print average radius
print(f"Average of r over samples: {np.mean(r_vals):.4f}")

