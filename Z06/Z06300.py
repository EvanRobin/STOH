import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
import math

# Parameters
n_steps = 200  # time steps in the animation
n_walkers = 1000  # number of Metropolis walkers
sigma = 2.0  # proposal distribution width
step_interval = 10  # how often we record a frame

# Hydrogen 3s orbital probability function
def prob(x, y, z):
    r = np.sqrt(x**2 + y**2 + z**2)
    return ((27 - 18*r + 2*r**2)**2) * np.exp(-2*r/3)

# Initialize all walkers at the origin
positions = np.zeros((n_steps, n_walkers, 3))
walkers = np.zeros((n_walkers, 3))

# Run Metropolis sampling for all walkers over time
for t in range(n_steps):
    for i in range(n_walkers):
        x, y, z = walkers[i]
        x_new = x + np.random.normal(0, sigma)
        y_new = y + np.random.normal(0, sigma)
        z_new = z + np.random.normal(0, sigma)

        p_new = prob(x_new, y_new, z_new)
        p_old = prob(x, y, z)

        if np.random.rand() < min(1, p_new / p_old):
            walkers[i] = [x_new, y_new, z_new]

    positions[t] = walkers

# Animate the walkers
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')
scat = ax.scatter([], [], [], s=1, alpha=0.5)

ax.set_xlim(-20, 20)
ax.set_ylim(-20, 20)
ax.set_zlim(-20, 20)
ax.set_title("Animated Hydrogen Atom - 3s Orbital")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.view_init(elev=30, azim=60)

def update(frame):
    data = positions[frame]
    scat._offsets3d = (data[:, 0], data[:, 1], data[:, 2])
    ax.set_title(f"Frame {frame}")
    return scat,

ani = animation.FuncAnimation(fig, update, frames=n_steps, interval=100, blit=False)
ani.save("hydrogen_3s.gif", writer='pillow', fps=10)
plt.show()
