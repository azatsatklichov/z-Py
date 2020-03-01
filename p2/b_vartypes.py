
'''
Created on Jan 6, 2018

@author: satklichov
'''
#!/usr/bin/python
from collections import OrderedDict

counter = 100  # An integer assignment
miles = 1000.00  # A floating point
name = "John"  # A string

print counter
print miles
print name                 

# multiple assignment
# all three variables are assigned to the same memory location.
a = b = c = 1
print a, b, c

#defines TUPLE
a = b = c = 1,
print a, b, c

a = b = c = 1, 2, 3
print a, b, c

x = y = z = 1,
print x, y, z

# You can also assign multiple objects to multiple variables. For example
a, b = "men a", 'men b'
print a, b

a, b, c = 1, 2, "john"
print a, b, c

var1 = 1
var2 = 10
print var1, var2

del var1
# print var1, var2
print  var2

# 4 different number types int, long, float, complex
a, b, c, d  = 10, 0xDEFABCECBDAECBFBAEl, 0.0, 3e+26J
print a,b,c,d 



#strings
_str = 'Hello World!'

print _str          # Prints complete string
print _str[0]       # Prints first character of the string
print _str[2:5]     # Prints characters starting from 3rd to 5th
print _str[2:]      # Prints string starting from 3rd character
print _str * 2      # Prints string two times
print _str *5      # Prints string 5 times
print _str + "TEST" # Prints concatenated string
print _str[3:]
print _str[1:4] #index ZERO based, left INCLUSIVE, right EXCLUSIVE, like MATH [1, 4)


#Python Lists
#To some extent, lists are similar to arrays in C. One difference between them is that all the items belonging to a _list can be of different data type.
#The values stored in a _list can be accessed using the slice operator ([ ]
_list = [ 'abcd', 786 , 2.23, 'john', 70.2 ]
tinylist = [123, 'john']

print _list          # Prints complete _list
print _list[0]       # Prints first element of the _list
print _list[1:3]     # Prints elements starting from 2nd till 3rd 
print _list[2:]      # Prints elements starting from 3rd element
print tinylist * 2  # Prints _list two times
print _list + tinylist # Prints concatenated lists
_list = [1, "sdd", 4]
print _list
print _list * 3
#print _list + "sds" + tinylist
print _list + tinylist
print _list[1:7]  #GOOD no Index out of bound exception
#print _list[7] #: _list index out of range


#Python Tuples  - READ ONLY lists
#A _tuple is another sequence data type that is similar to the _list.
#The main differences between lists and tuples are: Lists are enclosed in brackets ( [ ] ) and their elements and size can be changed, while tuples are enclosed in parentheses ( ( ) ) and cannot be updated.
_tuple = ( 'abcd', 786 , 2.23, 'john', 70.2  )
tinytuple = (123, 'john')
print _tuple           # Prints complete _list
print _tuple[0]        # Prints first element of the _list
print _tuple[1:3]      # Prints elements starting from 2nd till 3rd 
print _tuple[2:]       # Prints elements starting from 3rd element
print tinytuple * 2   # Prints _list two times
print _tuple + tinytuple # Prints concatenated lists
#or _tuple can be defined like
readOnly = 2,3,4,5
print readOnly
print readOnly[2:6] #no exception
print readOnly[2:3]
print readOnly[2:4]
print readOnly[2]
#readOnly[2] = 9 #TypeError: '_tuple' object does not support item assignment

#TUPLE can not be updated, ...
_tuple = ( 'abcd', 786 , 2.23, 'john', 70.2  )
_list = [ 'abcd', 786 , 2.23, 'john', 70.2  ]
#_tuple[2] = 1000    # Invalid syntax with _tuple
_list[2] = 1000     # Valid syntax with _list
print _list


#Python Dictionary Python's dictionaries are kind of hash table type. Like Hashmap in Java
#Values, on the other hand, can be any arbitrary Python object.

#not ordered 
_dict = {}
_dict['one'] = "This is one"
_dict[2]     = "This is two"
_dict["some more value"] = 66666
tinydict = {'name': 'john','code':6734, 'dept': 'sales'}


print _dict['one']       # Prints value for 'one' key
print _dict[2]           # Prints value for 2 key
print _dict["some more value"]
_dict["some more value"] = 777777
print _dict["some more value"] 
 
print tinydict          # Prints complete dictionary
print tinydict.keys()   # Prints all the keys
print tinydict.values() # Prints all the values
print tinydict.items() # pairs

print 
d2 = {}
d2['e'] = 'E'
d2['d'] = 'D'
d2['c'] = 'C'
d2['b'] = 'B'
d2['a'] = 'A'
print d2

d1 = OrderedDict()
d1['a'] = 'A'
d1['e'] = 'E'
d1['b'] = 'B'
d1['c'] = 'C'
d1['d'] = 'D'
print d1


print('Regular dictionary:')
d = {}
d['a'] = 'A'
d['b'] = 'B'
d['c'] = 'C'

for k, v in d.items():
    print(k, v)
    

print('\nOrderedDict:')
d = OrderedDict()
d['a'] = 'A'
d['b'] = 'B'
d['c'] = 'C'

for k, v in d.items():
    print(k, v)    




