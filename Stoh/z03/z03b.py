import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import PillowWriter

dx = 2.0
D = 1.5  # from z03a
dt = 0.1  # from dx^2 > 2Ddt

Nx = int(200.0 / dx)
Nt = int(200.0 / dt)
left, right = 0.0, 0.0 
alpha = D * dt / (dx ** 2)

dif1, dif2 = np.zeros(Nx + 1), np.zeros(Nx + 1)

def distribution(s):  
    if s > -0.8 * dx and s < 0.8 * dx:
        return 1.0 / dx
    else:
        return 0.0


for p in range(len(dif1)):
    dif1[p] = distribution(-100.0 + p * dx)

# Array to store values every int(1/dt)
Dif = np.zeros((200, Nx + 1))
Dif[0, :] = dif1

frame_idx = 1
for t in range(1, Nt):
    for x in range(1, Nx):
        dif2[x] = alpha * (dif1[x + 1] + dif1[x - 1]) + (1 - 2 * alpha) * dif1[x]
    dif2[0], dif2[-1] = left, right
    dif1 = np.copy(dif2)
    if t % int(1 / dt) == 0:
        Dif[frame_idx, :] = dif2
        frame_idx += 1


xpos = np.arange(-100.0, 100.0 + dx, dx)

fig = plt.figure(figsize=(10, 7), dpi=120)
metadata = dict(title="Diffusion")
plt.rcParams.update({'font.size': 15})
writer = PillowWriter(fps=10, metadata=metadata)
with writer.saving(fig, "diffusion.gif", 120):
    for j in range(200):
        plt.clf()
        plt.plot(xpos, Dif[j, :], lw=2.5, color='red', label='$\u03C1$(x,t)')
        plt.xlabel('$x$ / cm')
        plt.ylabel('$\u03C1$(x,t) / cm$^{-1}$')
        plt.legend(loc='upper right')
        plt.xlim(-100.0, 100.0)
        plt.ylim(0.0, 0.2)
        plt.text(65.0, 0.17, s='t={}s'.format(j), fontsize='medium')
        plt.grid(lw=0.3, linestyle=':')
        writer.grab_frame()