import numpy as np
import matplotlib.pyplot as plt

# Load data from file
data = np.loadtxt("E.txt")

# Choose the column you want (e.g., column 2)
observable = data[:, 1]  # Adjust index as needed

# Block averaging function
def block_average(data, max_block_size=None):
    N = len(data)
    if max_block_size is None:
        max_block_size = N // 10

    block_sizes = []
    std_errors = []

    for b in range(1, max_block_size + 1):
        n_blocks = N // b
        if n_blocks < 2:
            break
        reshaped = data[:n_blocks * b].reshape((n_blocks, b))
        block_means = np.mean(reshaped, axis=1)
        std_error = np.std(block_means, ddof=1) / np.sqrt(n_blocks)
        
        block_sizes.append(b)
        std_errors.append(std_error)

    return np.array(block_sizes), np.array(std_errors)

# Compute block statistics
block_sizes, std_errors = block_average(observable)

# Plot the result
plt.figure(figsize=(10, 6))
plt.plot(block_sizes, std_errors * 1e3, label='Standard error')  # scaled to mK
plt.xlabel("Block size (b)")
plt.ylabel(r"$10^3 \, \sigma_E$ / mK")
plt.title("Error estimation using block averaging")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()