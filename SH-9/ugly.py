import numpy as np
x = np.arange(10)
x2 = np.reshape(x, (2, 5))
print(x2, 'og')



np.roll(x2, -1, axis=0)
np.roll(x2, 1, axis=1)
print(np.roll(x2, axis=1))
np.roll(x2, (1, 1), axis=(1, 0))
np.roll(x2, (2, 1), axis=(1, 0))