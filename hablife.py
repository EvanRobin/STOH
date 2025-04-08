import numpy as numpy
import matplotlib.pyplot as pyplot
import random as rand

no = 1000.0
dt = 0.1
t = 1000
p = 0.02

to = 0.0
N=[]
time=[]

while to<=t:
    decay = rand.random()
    if decay < p:
        no-=1
    N.append(no)
    time.append(to)
    
    