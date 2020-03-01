'''
Created on Jan 7, 2018

@author: satklichov
'''
from click._compat import raw_input

# The dir() built-in function returns a sorted list of strings containing the names defined by a module.
# Import built-in module math

_str = raw_input("Enter your input: ");
print ("Received input is : ", _str)

######## input ########
# function is equivalent to raw_input, except that it assumes the input is a valid Python expression and returns the evaluated result to you
_str = input("Enter your input: ");
print ("Received input is : ", _str)
#Enter your input: [x*5 for x in range(2,10,2)]

