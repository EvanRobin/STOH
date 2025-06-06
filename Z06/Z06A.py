import numpy as np
import matplotlib.pyplot as plt
import math
 
# Parameters
n_steps = 100000
 
x = 0.0  # starting point
y = 0.0
z = 0.0
sigma = 2.0  # width
 
# P(x, y, z) = exp(-r / 2) where r = sqrt(x^2 + y^2 + z^2)
def prob(x, y, z):
    r = math.sqrt(x**2 + y**2 + z**2)
    return z**2*np.exp( -r )
 
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
 
#lot the samples
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x_vals, y_vals, z_vals, alpha=0.3, s=1)
ax.set_title("3D Metropolis Sampling")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.view_init(azim=60, elev=0)
plt.show()
 
print(f"Average of r over samples: {np.mean(r_vals):.4f}")