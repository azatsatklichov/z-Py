'''
Created on Jan 7, 2018

@author: satklichov
'''


#The dir() built-in function returns a sorted list of strings containing the names defined by a module.
# Import built-in module math
import math
import random
import sys

content = dir(math)
print (content)

content = dir(sys)
print (content)

content = dir(random)
print (content)

content = dir()
print (content)

