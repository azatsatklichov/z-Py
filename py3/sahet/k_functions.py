'''
Created on Jan 7, 2018

@author: satklichov
'''


# Function definition is here
def printme(_str):
   "This prints a passed string into this function"
   print (_str)
   return;


# Now you can call printme function
printme("I'm first call to user defined function!")
printme("Again second call to the same function")


# Function definition is here
def changeme(mylist):
   "This changes a passed list into this function"
   mylist.append([1, 2, 3, 4]);
   print ("Values inside the function: ", mylist)
   return


# Now you can call changeme function
mylist = [10, 20, 30];
changeme(mylist);
print ("Values outside the function: ", mylist)


# Function definition is here
def changeme2(mylist):
   "This changes a passed list into this function"
   mylist = [1, 2, 3, 4];  # This would assig new reference in mylist
   print ("Values inside the function: ", mylist)
   return


# Now you can call changeme function
mylist = [10, 20, 30];
changeme2(mylist);
print ("Values outside the function: ", mylist)

#!/usr/bin/python

print()

# Function definition is here
def printinfo( name, age ):
   "This prints a passed info into this function"
   print ("Name: ", name)
   print ("Age ", age)
   return;

# Now you can call printinfo function
printinfo( age=50, name="miki" )


print()

# Function definition is here
def printinfo2( name, age = 35 ):
   "This prints a passed info into this function"
   print ("Name: ", name)
   print ("Age ", age)
   return;

# Now you can call printinfo function
printinfo2( age=50, name="miki" )
printinfo2( name="miki" )

print()

# Function definition is here
def printinfo3( arg1, *vartuple ):
   "This prints a variable passed arguments"
   print ("Output is: ")
   print (arg1)
   for var in vartuple:
      print (var)
   return;

# Now you can call printinfo function
printinfo3( 10 )
printinfo3( 70, 60, 50 )
