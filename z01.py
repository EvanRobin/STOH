import random
from matplotlib import pyplot as plt

k = 5
minN = 100
maxN = 10000000

listOfN = [i for i in range(minN, maxN, 1000)]

y = []
randomNumbers = []

for i in range(maxN):
    randomNumbers.append(random.random())

I = 0
product = 0

for i in range(len(listOfN)):
    N = listOfN[i]
    for j in range(I, N - k):
        product += randomNumbers[j] * randomNumbers[j + k]

    c5 = product / N
    y.append(N**0.5 * abs(c5 - 0.25))
    I = N - k

plt.scatter(listOfN, y, s=0.1)
plt.xlabel("N")
plt.ylabel("sqrt(N)*c_5 - 1/4")
plt.title("C(5) test za random.random()")
plt.show()
