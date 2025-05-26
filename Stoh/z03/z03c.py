import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import PillowWriter
import matplotlib.ticker as tick

#  Parameters
Nw = 64000
Nt_walkers = 200
Dx = 2.0
walkers = np.zeros(Nw)
P = np.zeros((Nt_walkers, int(200.0/Dx)+1))  
r_MS, time = [0.0], [0]

# Diffusion 
dx = 2.0
D = 1.5
dt = 0.1
Nx = int(200.0/dx)
Nt_diff = int(200.0/dt)
alpha = D * dt / (dx**2)
left, right = 0.0, 0.0
dif1, dif2 = np.zeros(Nx+1), np.zeros(Nx+1)
rho = np.zeros((Nt_walkers, Nx+1))  



# Walkers
for t in range(Nt_walkers):
    r = 0.0
    prob = np.zeros(int(200.0/Dx)+1)
    for w in range(Nw):
        if t > 0:
            dx = -3.0 + 6*np.random.rand()
            walkers[w] += dx
        if -100.0 <= walkers[w] <= 100.0:
            i = int((walkers[w] + 100.0 + 0.5) / Dx)
            prob[i] += 1
            r += walkers[w]**2
    P[t] = prob / Nw / Dx
    if t > 0:
        r_MS.append(r/Nw)
        time.append(t)

# Diffusion 
dx = 2.0
D = 1.5
dt = 0.1
Nx = int(200.0/dx)
Nt_diff = int(200.0/dt)
alpha = D * dt / (dx**2)
left, right = 0.0, 0.0
dif1, dif2 = np.zeros(Nx+1), np.zeros(Nx+1)
rho = np.zeros((Nt_walkers, Nx+1))  # Match walker output steps

def distribution(s):
    return 1.0/dx if -0.8*dx < s < 0.8*dx else 0.0

for p in range(len(dif1)):
    dif1[p] = distribution(-100.0 + p*dx)
rho[0] = dif1.copy()

# Simulate diffusion
step = 0
for t in range(1, Nt_diff):
    for x in range(1, Nx):
        dif2[x] = alpha * (dif1[x+1] + dif1[x-1]) + (1 - 2*alpha) * dif1[x]
    dif2[0], dif2[-1] = left, right
    dif1 = dif2.copy()
    if t % int(1/dt) == 0:
        step += 1
        if step < Nt_walkers:
            rho[step] = dif2.copy()


xpos = np.arange(-100.0, 100.0 + dx, dx)
k = [5, 10, 15, 50]

text = (
    'walkers:   N=64000, x$_{i}$(t=0)=0.0\n\t\t$\u0394$x\u2208[-3,3] cm, $\u0394$t=1 s\n'
    'diffusion: D=1.5 cm$^{2}$s$^{-1}$, $\u03C1$(x,t=0)=$\u03B4$(x) cm$^{-1}$\n\t\t'
    '$\u0394$x=2.0 cm, $\u0394$t=0.1 s'
)

fig = plt.figure(figsize=(10,7), dpi=120)
metadata = dict(title="Distributions")
plt.rcParams.update({'font.size': 15})
writer = PillowWriter(fps=10, metadata=metadata)
with writer.saving(fig, "Walkers_Diffusion.gif", 120):
    for j in range(Nt_walkers):
        plt.clf()
        plt.plot(xpos, P[j], lw=1.0, color='red', label='P$_{walkers}$(x,t)')
        plt.plot(xpos, rho[j], lw=1.0, color='yellow', label='P$_{diffusion}$(x,t)')
        plt.xlabel('$x$ / cm')
        plt.ylabel('P(x,t) / cm$^{-1}$')
        plt.legend(loc='upper right')
        plt.xlim(-100.0, 100.0)
        plt.ylim(0.0, 0.05)
        plt.text(50.0, 0.039, s=f't={j}s', fontsize='medium')
        plt.text(-95.0, 0.039, s=text, fontsize='medium')
        plt.grid(lw=0.3, linestyle=':')
        writer.grab_frame()

# Static comparison at specific times
fig = plt.figure(figsize=(10,5), dpi=120)
axes = fig.add_axes([0.15, 0.15, 0.80, 0.80])
colors = ['blue', 'yellow', 'green', 'red']
for idx, t in enumerate(k):
    axes.plot(xpos, P[t], lw=1.0, color=colors[idx], label=f'P$_{{walkers}}$(x,t={t}s)')
    axes.plot(xpos, rho[t], lw=1.0, linestyle='-.', color=colors[idx], label=f'P$_{{diffusion}}$(x,t={t}s)')

axes.set_xlim(-60.0, 60.0)
axes.set_ylim(0.0, 0.12)
axes.set_xlabel('x / cm')
axes.set_ylabel('P(x,t) / cm$^{-1}$')
axes.xaxis.set_major_locator(tick.MultipleLocator(10))
axes.yaxis.set_major_locator(tick.MultipleLocator(1e-2))
axes.grid(lw=0.2, linestyle=':')
axes.legend()
plt.show()