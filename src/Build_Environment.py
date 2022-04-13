# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

# Veg, Tree, Water, Soil
AGENTS = [0,1,3]
N, M = 100, 100

dens = .8

E = np.random.choice(AGENTS, p=[dens*.5, dens*.5, 1-dens], size=N*M).reshape(N,M)

W = 3
water = [(x,y) for x,y in zip(np.random.randint(0,N,W), np.random.randint(0,M,W))]

for i,j in water:
    r = np.random.randint(4,30)
    
    for k in range(N):
        for l in range(M):
            if (i-k)**2+(j-l)**2 <= r**2:
                E[k,l]=2  
        
plt.imshow(E)
plt.show()

# If you wish to save it, uncomment this
#np.save("E/density_{}.npy".format(dens), E)