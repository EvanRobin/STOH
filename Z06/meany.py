import numpy as np
import matplotlib.pyplot as plt
import math

# Parameters
n_steps = 10000
blocks = 200
sigma = 2.0  # width

# Initialize starting point
x, y, z = 0.0, 0.0, 0.0

# P(x, y, z) = |3, 0, 0> orbital
def prob(x, y, z):
    r = math.sqrt(x**2 + y**2 + z**2)
    return ((27 - 18*r + (2*r**2))**2)*np.exp(-2r/3)

r_mean = []
r_mean_mean = []
block = []

# Metropolis
def loopty(n, x0, y0, z0):
    x = x0
    y = y0
    z = z0

    r_vals = []

    for _ in range(n):
        x_new = x + np.random.normal(0, sigma)
        y_new = y + np.random.normal(0, sigma)
        z_new = z + np.random.normal(0, sigma)

        p_new = prob(x_new, y_new, z_new)
        p_old = prob(x, y, z)

        acceptance_ratio = p_new / p_old if p_old > 0 else 1.0

        if np.random.rand() < acceptance_ratio:
            x, y, z = x_new, y_new, z_new

        r_vals.append(math.sqrt(x**2 + y**2 + z**2))

    return np.mean(r_vals)

# blocks
for i in range(blocks):
    r_mean.append(loopty(n_steps, x, y, z))
    r_mean_mean.append(np.mean(r_mean))
    block.append(i)

# Plot
plt.plot(block, r_mean_mean, label='Cumulative Mean of r')
plt.plot(block, r_mean, label='Singular Block Mean of r')
plt.xlabel('Block')
plt.ylabel('Mean r')
plt.legend()
plt.show()
