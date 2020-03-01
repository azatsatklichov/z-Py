'''
Created on Jan 7, 2018

@author: satklichov

The Common Gateway Interface, or CGI, is a set of standards that define how information 
is exchanged between the web server and a custom script. 

The CGI specs are currently maintained by the NCSA.
'''
import os

print ("Content-type: text/html\r\n\r\n")
print ("<font size=+1>Environment</font><\br>")
for param in os.environ.keys():
   print ("<b>%20s</b>: %s<\br>" % (param, os.environ[param]))
   
