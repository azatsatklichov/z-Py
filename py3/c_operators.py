a = 15
b = 8
print(a**b)   #to the power 20

print(a/b) # 5/2 = 2.5
print(a //b) #quotient 5/2 = 2


a = 3
b = 4
print(a**b)   #to the power 20

a = 15.77
b = 8
print(a**b)   #to the power 20

print()
#Bitwise operator works on bits and performs bit by bit operation. 
a = int('01100000', 2) #00111100 
b = int('00100110', 2) #00001101

#-----------------
print(bin(a&b)) # 00001100  print(a&b)
print(bin(a|b))  #00111101 print(a|b)
print(bin(a^b))  # 00110001 print(a^b)
print(bin(~a))  #11000011 print(~a)


a = 21
b = 10
c = 0

if ( a == b ):
   print("Line 1 - a is equal to b")
else:
   print("Line 1 - a is not equal to b")

if ( a != b ):
   print("Line 2 - a is not equal to b")
else:
   print("Line 2 - a is equal to b")


if ( a < b ):
   print("Line 4 - a is less than b") 
else:
   print("Line 4 - a is not less than b")

if ( a > b ):
   print("Line 5 - a is greater than b")
else:
   print("Line 5 - a is not greater than b")

a = 5;
b = 20;
if ( a <= b ):
   print("Line 6 - a is either less than or equal to  b")
else:
   print("Line 6 - a is neither less than nor equal to  b")

if ( b >= a ):
   print("Line 7 - b is either greater than  or equal to b")
else:
   print("Line 7 - b is neither greater than  nor equal to b")


a = 21
b = 10
c = 0

c = a + b
print("Line 1 - Value of c is ", c)

c += a
print("Line 2 - Value of c is ", c) 

c *= a
print("Line 3 - Value of c is ", c) 

c /= a 
print("Line 4 - Value of c is ", c) 


c  = 2
c %= a
print("Line 5 - Value of c is ", c)

c **= a
print("Line 6 - Value of c is ", c)

c //= a
print("Line 7 - Value of c is ", c)


a = 60            # 60 = 0011 1100 
b = 13            # 13 = 0000 1101 
c = 0

c = a & b;        # 12 = 0000 1100
print("Line 1 - Value of c is ", c)

c = a | b;        # 61 = 0011 1101 
print("Line 2 - Value of c is ", c)

c = a ^ b;        # 49 = 0011 0001
print("Line 3 - Value of c is ", c)

c = ~a;           # -61 = 1100 0011
print("Line 4 - Value of c is ", c)

c = a << 2;       # 240 = 1111 0000 --> 60*2^2
print("Line 5 - Value of c is ", c)

c = a >> 2;       # 15 = 0000 1111 --> 60/2^2
print("Line 6 - Value of c is ", c)


#IN, not IN
a = 44
b = 20
list = [1, 2, 3, 4, 5 ];

if ( a in list ):
   print("Line 1 - a is available in the given list")
else:
   print("Line 1 - a is not available in the given list")

if ( b not in list ):
   print("Line 2 - b is not available in the given list")
else:
   print("Line 2 - b is available in the given list")


a = 2
if ( a in list ):
   print("Line 3 - a is available in the given list")
else:
   print("Line 3 - a is not available in the given list")
   
c = 5
if a in list:
    print("URRAAAAAA")
    

#Identity operators compare the memory locations of two objects. There are two Identity operators as explained below
a = 20
b = 20

if ( a is b ):
   print("Line 1 - a and b have same identity")
else:
   print("Line 1 - a and b do not have same identity")

if ( id(a) == id(b) ):
   print("Line 2 - a and b have same identity")
else:
   print("Line 2 - a and b do not have same identity")
   
if ( a == b ):
   print("Line X - a and b are equal")
else:
   print("Line X - a and b do not have same identity")



b = 30
if ( a is b ):
   print("Line 3 - a and b have same identity")
else:
   print("Line 3 - a and b do not have same identity")

if ( a is not b ):
   print("Line 4 - a and b do not have same identity")
else:
   print("Line 4 - a and b have same identity")
   
   
a = 20
b = 10
c = 15
d = 5
e = 0

e = (a + b) * c / d       #( 30 * 15 ) / 5
print("Value of (a + b) * c / d is ", e)

e = ((a + b) * c) / d     # (30 * 15 ) / 5
print("Value of ((a + b) * c) / d is ", e)

e = (a + b) * (c / d);    # (30) * (15/5)
print("Value of (a + b) * (c / d) is ", e)

e = a + (b * c) / d;      #  20 + (150/5)
print("Value of a + (b * c) / d is ", e)

