import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as tick
from scipy import stats as S
from matplotlib.animation import PillowWriter

Nw = 64000
Nt = 200
Dx = 2.0
walkers = np.zeros(Nw)
r_MS, time = [0.0], [0]

# Create a 2D array to store probabilities over time
P = np.zeros((Nt, int(200.0/Dx)+1))

# Initial probability distribution
prob0 = np.zeros(int(200.0/Dx)+1)
for w in range(Nw):
    i = int((walkers[w]+100.0)/Dx)
    prob0[i] += 1
for x in range(int(200.0/Dx)+1):
    P[0, x] = prob0[x] / Nw

# Evolve probability distribution
t = 1
while t < Nt:
    r = 0.0
    prob = np.zeros(int(200.0/Dx)+1)
    for w in range(Nw):
        dx = -3.0 + 6*np.random.rand()
        walkers[w] += dx
        if walkers[w] >= -100.0 and walkers[w] <= 100.0:
            i = int((walkers[w]+100.0+0.5)/Dx)
            prob[i] += 1
            r += walkers[w]**2
    for x in range(int(200.0/Dx)+1):
        P[t, x] = prob[x] / Nw / Dx
    r_MS.append(r / Nw)
    time.append(t)
    t += 1

# Fit and plot <r²>
const, b, r, p, std_err = S.linregress(time, r_MS)
D = const / 2
X = np.arange(0.0, Nt+0.5, 0.5)
Y = [const * p for p in X]
'''
fig = plt.figure(figsize=(12,6), dpi=120)
axes = fig.add_axes([0.15, 0.15, 0.75, 0.75])
plt.rcParams.update({'font.size': 10})
axes.plot(X, Y, lw=1.0, color='blue', label='<r$^{2}$(t)>=2Dt - fit')
axes.scatter(time, r_MS, facecolor='none', edgecolor='red', s=5.0, label='MC data')
axes.set_xlim(0.0, Nt)
axes.set_ylim(0.0, 600.0)
axes.set_xlabel('t / s')
axes.set_ylabel('<r$^{2}$(t)> / cm$^{2}$')
axes.xaxis.set_major_locator(tick.MultipleLocator(20))
axes.yaxis.set_major_locator(tick.MultipleLocator(50))
axes.grid(lw=0.2, linestyle=':')
axes.legend()
plt.show()
'''
# Animate the probability distribution
xpos = np.arange(-100.0, 100.0+Dx, Dx)
fig = plt.figure(figsize=(10,7), dpi=120)
metadata = dict(title="Walkers probability")
plt.rcParams.update({'font.size': 15})
writer = PillowWriter(fps=10, metadata=metadata)
with writer.saving(fig, "probability.gif", 120):
    for t in range(Nt):
        plt.clf()
        plt.plot(xpos, P[t, :], lw=2.5, color='red', label='P$_{1D}$(x,t)')
        plt.xlabel('$x$ / cm')
        plt.ylabel('P$_{1D}$(x,t) / cm$^{-1}$')
        plt.legend(loc='upper right')
        plt.xlim(-100.0, 100.0)
        plt.ylim(0.0, 0.2)
        plt.text(65.0, 0.17, s='t={}s'.format(t), fontsize='medium')
        plt.grid(lw=0.3, linestyle=':')
        writer.grab_frame()