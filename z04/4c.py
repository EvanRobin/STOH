import numpy as np
import matplotlib.pyplot as plt

def simulate_decay(dt):
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

    t_max = 60  # total simulation time in minutes
    steps = int(t_max / dt)

    sb_counts = []
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
        time.append(t)

    return np.array(time), np.array(sb_counts)

# Run simulations for different dt values
dt_values = [0.1, 5.0]
results = {}

for dt in dt_values:
    time, sb_counts = simulate_decay(dt)
    results[dt] = (time, sb_counts)

# Plot comparison
plt.figure(figsize=(10, 6))

for dt in dt_values:
    time, sb_counts = results[dt]
    plt.plot(time, sb_counts, marker='.', linestyle='-', label=f'dt = {dt} min')

# Add analytical solution
lambda1 = np.log(2) / 2.5
time_analytical = np.linspace(0, 60, 600)
N0 = 1000
sb_analytical = N0 * np.exp(-lambda1 * time_analytical)
plt.plot(time_analytical, sb_analytical, 'k--', label='Analytical 133Sb')

plt.xlabel("Time (minutes)")
plt.ylabel("Number of 133Sb atoms")
plt.title("133Sb Decay Comparison at Different Time Steps")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()