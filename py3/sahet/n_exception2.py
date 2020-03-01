'''
Created on Jan 7, 2018

@author: satklichov
'''


#!/usr/bin/python
try:
   fh = open("testfile", "w")
   fh.write("This is my test file for exception handling!! hh")
except IOError:
   print ("Error: can\'t find file or read data")
else:
   print ("Written content in the file successfully")
   fh.close()

try:
   fh = open("testfile", "r")
   fh.write("This is my test file for exception handling!! oo")
except IOError:
   print ("Error: can\'t find file or read data")
else:
   print ("Written content in the file successfully")

try:
   fh = open("testfile", "w")
   fh.write("This is my test file for exception handling!! pp")
finally:
   print ("Error: can\'t find file or read data")

