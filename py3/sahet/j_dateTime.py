'''
Created on Jan 7, 2018

@author: satklichov
'''

#!/usr/bin/python
import time;  # This is required to include time module.

ticks = time.time()
print ("Number of ticks since 12:00am, January 1, 1970:", ticks)

localtime = time.localtime(time.time())
print ("Local current time :", localtime) 


#formatted
localtime = time.asctime( time.localtime(time.time()) )
print ("Local current time :", localtime)

print()

import calendar
# cal = calendar.month(2008, 1)
cal = calendar.month(2019, 11)
print ("Here is the calendar:")
print (cal)

