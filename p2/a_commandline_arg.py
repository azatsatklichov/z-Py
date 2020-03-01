'''
Created on Jan 6, 2018

@author: satklichov
'''

#!/usr/bin/python

import sys
from __builtin__ import _dict

x = _dict()
x[7] = "dsd"
x[2] = 33
print x

#NOTE As mentioned above, first argument is always script name and it is also being counted in number of arguments.
print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', _str(sys.argv)