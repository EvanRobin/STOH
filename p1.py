import numpy as np
import random
import matplotlib.pyplot as plt
"""
random_list = []
for i in range(0, 2*10**5):
    random_list.append(random.random()*random.random())

print(random_list)
""" 
random_listx = []
random_listy = []
for i in range(0, 2*10**4):
    random_listx.append(random.random())
    random_listy.append(random.random())

plt.scatter(random_listx, random_listy)
plt.show()