print "abs(-45) : ", abs(-45)
print "abs(100.12) : ", abs(100.12)
print "abs(119L) : ", abs(119L)

print "min(80, 100, 1000) : ", min(80, 100, 1000)
print "min(-20, 100, 400) : ", min(-20, 100, 400)
print "min(-80, -20, -10) : ", min(-80, -20, -10)
print "min(0, 100, -400) : ", min(0, 100, -400)

#or via math lib
import math   # This will import math module

print "math.fabs(-45.17) : ", math.fabs(-45.17)
print "math.fabs(100.12) : ", math.fabs(100.12)
print "math.fabs(100.72) : ", math.fabs(100.72)
print "math.fabs(119L) : ", math.fabs(119L)
print "math.fabs(math.pi) : ", math.fabs(math.pi)


print



print "math.ceil(-45.17) : ", math.ceil(-45.17)
print "math.ceil(100.12) : ", math.ceil(100.12)
print "math.ceil(100.72) : ", math.ceil(100.72)
print "math.ceil(119L) : ", math.ceil(119L)
print "math.ceil(math.pi) : ", math.ceil(math.pi)

print

print "math.floor(-45.17) : ", math.floor(-45.17)
print "math.floor(100.12) : ", math.floor(100.12)
print "math.floor(100.72) : ", math.floor(100.72)
print "math.floor(119L) : ", math.floor(119L)
print "math.floor(math.pi) : ", math.floor(math.pi)

print

print "cmp(80, 100) : ", cmp(80, 100)
print "cmp(180, 100) : ", cmp(180, 100)
print "cmp(-80, 100) : ", cmp(-80, 100)
print "cmp(80, -100) : ", cmp(80, -100)
print "cmp(80, 80) : ", cmp(80, 80)

print

#e^x
print "math.exp(-45.17) : ", math.exp(-45.17)
print "math.exp(100.12) : ", math.exp(100.12)
print "math.exp(100.72) : ", math.exp(100.72)
print "math.exp(119L) : ", math.exp(119L)
print "math.exp(math.pi) : ", math.exp(math.pi)



print
print "math.log(100.12) : ", math.log(100.12)
print "math.log(100.72) : ", math.log(100.72)
print "math.log(119L) : ", math.log(119L)
print "math.log(math.pi) : ", math.log(math.pi)


print "math.log10(100.12) : ", math.log10(100.12)
print "math.log10(100.72) : ", math.log10(100.72)
print "math.log10(119L) : ", math.log10(119L)
print "math.log10(math.pi) : ", math.log10(math.pi)

print


print "max(80, 100, 1000) : ", max(80, 100, 1000)
print "max(-20, 100, 400) : ", max(-20, 100, 400)
print "max(-80, -20, -10) : ", max(-80, -20, -10)
print "max(0, 100, -400) : ", max(0, 100, -400)



#The method modf() returns the fractional and integer parts of x in a two-item tuple.
print "math.modf(100.12) : ", math.modf(100.12)
print "math.modf(100.72) : ", math.modf(100.72)
print "math.modf(119L) : ", math.modf(119L)
print "math.modf(math.pi) : ", math.modf(math.pi)

print
print "math.pow(100, 2) : ", math.pow(100, 2)
print "math.pow(100, -2) : ", math.pow(100, -2)
print "math.pow(2, 4) : ", math.pow(2, 4)
print "math.pow(3, 0) : ", math.pow(3, 0)


print
#The method round() returns x rounded to n digits from the decimal point.
print "round(80.23456, 2) : ", round(80.23456, 2)
print "round(100.000056, 3) : ", round(100.000056, 3)
print "round(-100.000056, 3) : ", round(-100.00005683, 5)


print
print "math.sqrt(100) : ", math.sqrt(100)
print "math.sqrt(7) : ", math.sqrt(7)
print "math.sqrt(math.pi) : ", math.sqrt(math.pi)

print
#The method choice() returns a random item from a list, tuple, or string
import random

print "choice([1, 2, 3, 5, 9]) : ", random.choice([1, 2, 3, 5, 9])
print "choice('A String') : ", random.choice('A String')

# Select an even number in 100 <= number < 1000
print "randrange(100, 1000, 2) : ", random.randrange(100, 1000, 2)

# Select another number in 100 <= number < 1000
print "randrange(100, 1000, 3) : ", random.randrange(100, 1000, 3)

# First random number
print "random() : ", random.random()

# Second random number
print "random() : ", random.random()

print 


#The method seed() sets the integer starting value used in generating random numbers. 
random.seed( 10 )
print "Random number with seed 10 : ", random.random()

# It will generate same random number
random.seed( 10 )
print "Random number with seed 10 : ", random.random()

# It will generate same random number
random.seed( 10 )
print "Random number with seed 10 : ", random.random()



list = [20, 16, 10, 5];
print "Not shuffled list : ",  list
random.shuffle(list)
print "Reshuffled list : ",  list
random.shuffle(list)
print "Reshuffled list : ",  list


# The method uniform() returns a random float r, such that x is less than or equal to r and r is less than y.

print "Random Float uniform(5, 10) : ",  random.uniform(5, 10)
print "Random Float uniform(7, 14) : ",  random.uniform(7, 14)

print

print "acos(0.64) : ",  math.acos(0.64)
print "acos(0) : ",  math.acos(0)
print "acos(-1) : ",  math.acos(-1)
print "acos(1) : ",  math.acos(1)

print "asin(0.64) : ",  math.asin(0.64)
print "asin(0) : ",  math.asin(0)
print "asin(-1) : ",  math.asin(-1)
print "asin(1) : ",  math.asin(1)

print "atan(0.64) : ",  math.atan(0.64)
print "atan(0) : ",  math.atan(0)
print "atan(10) : ",  math.atan(10)
print "atan(-1) : ",  math.atan(-1)
print "atan(1) : ",  math.atan(1)

print "atan2(-0.50,-0.50) : ",  math.atan2(-0.50,-0.50)
print "atan2(0.50,0.50) : ",  math.atan2(0.50,0.50)
print "atan2(5,5) : ",  math.atan2(5,5)
print "atan2(-10,10) : ",  math.atan2(-10,10)
print "atan2(10,20) : ",  math.atan2(10,20)

print "cos(3) : ",  math.cos(3)
print "cos(-3) : ",  math.cos(-3)
print "cos(0) : ",  math.cos(0)
print "cos(math.pi) : ",  math.cos(math.pi)
print "cos(2*math.pi) : ",  math.cos(2*math.pi)


print 
# The method hypot() return the Euclidean norm, sqrt(x*x + y*y).
print "hypot(3, 2) : ",  math.hypot(3, 2)
print "hypot(-3, 3) : ",  math.hypot(-3, 3)
print "hypot(0, 2) : ",  math.hypot(0, 2)

print 
print "tan(3) : ",  math.tan(3)
print "tan(-3) : ",  math.tan(-3)
print "tan(0) : ",  math.tan(0)
print "tan(math.pi) : ",  math.tan(math.pi)
print "tan(math.pi/2) : ",  math.tan(math.pi/2)
print "tan(math.pi/4) : ",  math.tan(math.pi/4)


print "sin(3) : ",  math.sin(3)
print "sin(-3) : ",  math.sin(-3)
print "sin(0) : ",  math.sin(0)
print "sin(math.pi) : ",  math.sin(math.pi)
print "sin(math.pi/2) : ",  math.sin(math.pi/2)


print
#The method degrees() converts angle x from radians to degrees.
print "degrees(3) : ",  math.degrees(3)
print "degrees(180) : ",  math.degrees(180)
print "degrees(-3) : ",  math.degrees(-3)
print "degrees(0) : ",  math.degrees(0)
print "degrees(math.pi) : ",  math.degrees(math.pi)
print "degrees(math.pi/2) : ",  math.degrees(math.pi/2)
print "degrees(math.pi/4) : ",  math.degrees(math.pi/4)

print
#The method radians() converts angle x from degrees to radians.
print "radians(3) : ",  math.radians(3)
print "radians(-3) : ",  math.radians(-3)
print "radians(0) : ",  math.radians(0)
print "radians(math.pi) : ",  math.radians(math.pi)
print "radians(math.pi/2) : ",  math.radians(math.pi/2)
print "radians(math.pi/4) : ",  math.radians(math.pi/4)











