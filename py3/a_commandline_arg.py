'''
Created on Jan 6, 2018

@author: satklichov
'''

#!/usr/bin/python

import sys

x = dict()
x[7] = "dsd"
x[2] = 33
print(x)

print(x[2])
# print(x[1:])
print()
#NOTE As mentioned above, first argument is always script name and it is also being counted in number of arguments.
print('Number of arguments:', len(sys.argv), 'arguments.')
script_name = str(sys.argv)
print('Argument List:', script_name)
print("This is cool, because you have the path of file already: "+script_name[0:33])
