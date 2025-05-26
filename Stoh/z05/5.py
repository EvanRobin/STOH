import numpy as np

# Number of samples
n1 = 5000000
n2 = 500000

# Normalization constant for p(x) = A * exp(-x)
A = np.exp(1) / (np.exp(1) - 1)

# Distribution p(x) = 1 (uniform)
x1 = np.random.random(n1)
Fn1 = np.exp(-x1**2)
mean_Fn1 = np.mean(Fn1)
var1 = np.var(Fn1, ddof=0)

# Distribution p(x) = A * exp(-x)
r2 = np.random.random(n2)
x2 = -np.log(1 - r2 / A)  # Inverse transform sampling
Fn2 = np.exp(-x2**2) / (A * np.exp(-x2))
mean_Fn2 = np.mean(Fn2)
var2 = np.var(Fn2, ddof=0)

# Standard error
stderr1 = var1 / np.sqrt(n1)
stderr2 = var2 / np.sqrt(n2)

# Print results
print(f"{'n (samples)':<15}{n1:>12}{n2:>12}")
print(f"{'Mean F':<15}{mean_Fn1:12.7f}{mean_Fn2:12.7f}")
print(f"{'Variance':<15}{var1:12.7f}{var2:12.7f}")
print(f"{'StdErr':<15}{stderr1:12.7f}{stderr2:12.7f}")
