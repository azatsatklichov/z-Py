'''
Created on Jun 2, 2018

@author: ASUS
'''
#!/usr/bin/python
import sys

print('Number of arguments:', len(sys.argv), 'arguments.')
print('Argument List:', str(sys.argv))
print('argv[0] = ', str(sys.argv[0]))

print('argv[2] = ', str(sys.argv[2]) + "\n")

for st in sys.argv:
    print(st)

print("\nNOTE - As mentioned above, first argument is always script name and it is also being counted in number of arguments.")
