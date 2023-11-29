#https://www.w3schools.com/python/numpy/default.asp

#NumPy is used for working with arrays  like lodash for TS
#pip install numpy

#Matplotlib is a low level graph plotting library in python that serves as a visualization utility.
import matplotlib.pyplot as plt
import numpy as np

xpoints = np.array([0, 6])
ypoints = np.array([0, 250])

plt.plot(xpoints, ypoints)
plt.show()