import matplotlib.pyplot as plt
import numpy as np

alpha_1e3 = [4.6952, 4.2834, 5.1805, 4.3177, 4.7781, 5.0365, 4.3075, 4.0234, 4.3556, 4.5319]
alpha_1e4 = [4.6547, 6.5193, 5.8451, 5.1044, 5.4701, 5.5008, 4.9367, 5.1499, 5.7206, 4.9853]
alpha_1e5 = [6.3691, 8.8835, 5.8690, 6.0638, 5.9861, 6.5003, 5.7419, 5.7092, 6.7684, 7.2136]
alpha_1e6 = [5.9379, 6.2045, 6.7826, 6.7849, 6.6719, 6.1580, 6.4582, 6.2822, 6.6699, 7.4623]

# Step counts and mean alpha values
steps = [1e3, 1e4, 1e5, 1e6]
mean_alphas = [
    np.mean(alpha_1e3),
    np.mean(alpha_1e4),
    np.mean(alpha_1e5),
    np.mean(alpha_1e6),
]

# Plot
plt.figure(figsize=(8, 6))
plt.plot(steps, mean_alphas, marker='o', linestyle='-', color='b')
plt.xscale('log')
plt.xlabel('Simulation Steps (log scale)')
plt.ylabel('Average Estimated Alpha')
plt.title('Average Estimated Alpha vs. Simulation Steps')
plt.grid(True)
plt.tight_layout()
plt.show()