#https://www.w3schools.com/python/numpy/default.asp

#NumPy is used for working with arrays  like lodash for TS
#pip install numpy
import numpy as np

from numpy import random
import matplotlib.pyplot as plt
import seaborn as sns

arr = np.array([1, 2, 3, 4, 5])

print(arr)

#The main difference between a copy and a view of an array is that the copy is a new array, and the view is just a view of the original array.

arr = np.array([1, 2, 3, 4, 5])
x = arr.view()
arr[0] = 42

print(arr)
print(x)

arr = np.array([1, 2, 3, 4, 5])
x = arr.copy()
arr[0] = 42

print(arr)
print(x)

arr = np.array([1, 2, 3, 4, 5, 4, 4])

x = np.where(arr == 4)

print(x)



arr = np.array([3, 2, 0, 1])

print(np.sort(arr))

arr = np.array([41, 42, 43, 44])

x = [True, False, True, False]

newarr = arr[x]

print(newarr)

arr = np.array([41, 42, 43, 44])

# Create an empty list
filter_arr = []


#https://www.w3schools.com/python/numpy/numpy_random_seaborn.asp

# go through each element in arr
for element in arr:
  # if the element is higher than 42, set the value to True, otherwise False:
  if element > 42:
    filter_arr.append(True)
  else:
    filter_arr.append(False)

newarr = arr[filter_arr]

print(filter_arr)
print(newarr)



x = random.logistic(loc=1, scale=2, size=(2, 3))

print(x)
sns.distplot(random.logistic(size=1000), hist=False)

plt.show()