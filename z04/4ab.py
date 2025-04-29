import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Initial conditions
N0_sb = 1000
N0_te = 0
N0_i  = 0
N_sb = N0_sb
N_te = N0_te
N_i = N0_i

# Half-lives in minutes
t_half_sb = 2.5
t_half_te = 12.5

# Convert half-lives to decay constants
lambda1 = np.log(2) / t_half_sb
lambda2 = np.log(2) / t_half_te

dt = 0.1  # time step in minutes
t_max = 60  # total simulation time in minutes
steps = int(t_max / dt)

sb_counts = []
te_counts = []
i_counts = []
time = []

for step in range(steps):
    t = step * dt

    p1 = 1 - np.exp(-lambda1 * dt)
    p2 = 1 - np.exp(-lambda2 * dt)

    decayed_sb = np.random.binomial(N_sb, p1)
    decayed_te = np.random.binomial(N_te, p2)

    N_sb -= decayed_sb
    N_te += decayed_sb - decayed_te
    N_i  += decayed_te

    sb_counts.append(N_sb)
    te_counts.append(N_te)
    i_counts.append(N_i)
    time.append(t)

# Fit decay curve to estimate decay constants
def decay_fit(t, N0, lambd):
    return N0 * np.exp(-lambd * t)

# Fit Sb
popt_sb, _ = curve_fit(decay_fit, time, sb_counts, p0=[N0_sb, 0.1])
est_lambda1 = popt_sb[1]

# Fit Te decay
te_fit = np.array(te_counts)
popt_te, _ = curve_fit(decay_fit, time, te_fit + 1e-3, p0=[max(te_counts), 0.1])
est_lambda2 = popt_te[1]


print(f"Estimated decay constant for 133Sb: lambda1 = {est_lambda1:.4f} (true: {lambda1:.4f})")
print(f"Estimated decay constant for 133Te: lambda2 = {est_lambda2:.4f} (true: {lambda2:.4f})")

def exclude_first_n(lst, n):
    return lst[n:]

# Fit Te decay again for Te
te_fit2 = np.array(exclude_first_n(te_counts, 200))
te_fit2 = np.array(te_counts[200:])
time_fit2 = np.array(time[200:])  # match time array

popt_te, _ = curve_fit(decay_fit, time_fit2, te_fit2 + 1e-3, p0=[max(te_counts), 0.1])
est_lambda2_2 = popt_te[1]
print(f"Estimated decay constant for 133Te if we first wait a bit : lambda2 = {est_lambda2_2:.4f} (true: {lambda2:.4f})")

# Plotting

time_array = np.array(time)
N0 = N0_sb  # initial amount of Sb

N_sb_analytical = N0 * np.exp(-lambda1 * time_array)
N_te_analytical = N0 * (lambda1 / (lambda2 - lambda1)) * (np.exp(-lambda1 * time_array) - np.exp(-lambda2 * time_array))
N_i_analytical  = N0 * (1 - (lambda2 * np.exp(-lambda1 * time_array) - lambda1 * np.exp(-lambda2 * time_array)) / (lambda2 - lambda1))

# Plotting simulation vs. analytical
plt.figure(figsize=(10, 6))
plt.plot(time, sb_counts, 'b.', alpha=0.5, label='Simulated 133Sb')
plt.plot(time, te_counts, 'r.', alpha=0.5, label='Simulated 133Te')
plt.plot(time, i_counts,  'g.', alpha=0.5, label='Simulated 133I')

plt.plot(time_array, N_sb_analytical, 'b-', label='Analytical 133Sb')
plt.plot(time_array, N_te_analytical, 'r-', label='Analytical 133Te')
plt.plot(time_array, N_i_analytical,  'g-', label='Analytical 133I')

plt.xlabel("Time (minutes)")
plt.ylabel("Number of atoms")
plt.title("Monte Carlo vs. Analytical: 133Sb → 133Te → 133I")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()