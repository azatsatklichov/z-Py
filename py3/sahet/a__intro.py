#!/usr/bin/python

i = 2

while(i < 100):
    #i = "sas" NOT good, use Casting to define TYPE
    #print(i+"---")
    j = 2
    while(j <= (i/j)):
        print("(i,j) = (", i, ',', j, ')', j <= (i / j))
        if not(i%j): break
        j = j + 1
    if (j > i/j) : print(i, " is prime")
    i = i + 1

print("Good bye!")

print("\nCasting")
print("--- If you want to specify the data type of a variable, this can be done with casting. ---")

x = str(3)    # x will be '3'
y = int(3)    # y will be 3
z = float(3)  # z will be 3.0
print(type(x))
print(type(y))
print(type(z))

print(x)
x = 8; #still Dynamic typing is riskin in Paython, like Javascript (Typescript gives compile time issue_ 
print(x)

x = 5
y = "John"
print(type(x))
print(type(y))


x, y, z = "Orange", "Banana", "Cherry"
#x, y, z = "Orange", "Banana"    ValueError: not enough values to unpack (expected 3, got 2)
print(x)
print(y) 
print(z)
 
 
print('\nUnpack a Collection')
fruits = ["alma", "enar", "ulje"]  
print(fruits)

x, y, z  = fruits
#x, y  = fruits ##ValueError: too many values to unpack (expected 2)
print(x)
print(y)
print(z)
#Output Variables
print(x, y, z)
print(x + y + z)



x = 5
y = "John"
#print(x + y) or print(y+5) #TypeError: unsupported operand type(s) for +: 'int' and 'str'

#The best way to output multiple variables in the print() function is to separate them with commas, which even support different data types:
print(x, y) #displays with empty space between 



print('\nPython - Global Variables')
#like in JS/TS - Variables that are created outside of a function (as in all of the examples above) are known as global variables.

x = "awesome"

def myfunc():
    print("Python is " + x)

myfunc()


 
#just shadowing example
def myfunc2():
    x = "fantastic"
    print("Python is " + x)
    x +=  "fantastic" 
    print("Python is " + x)
    global xx
    xx = "I am global define in function"
    print("  " +xx)

myfunc2()
print("  " +xx)
print("Python is " + x)
