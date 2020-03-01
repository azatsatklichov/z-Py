
count = 0
while (count < 9):
    print('The count is:', count)
    if count is 6:
        count = 8
        continue   
    count = count + 1

print("Good bye!")

count = 0
while count < 5:
    print(count, " is  less than 5")
    count = count + 1
else:
    print(count, " is not less than 5")

for letter in 'Pythonzz':  # First Example
    print('Current Letter :', letter)

fruits = ['banana', 'apple', 'mango']
print(fruits)
for fruit in fruits:  # Second Example
    print('Current fruit :', fruit)

fruits = 'banana', 'apple', 'mango', 'alma'  # TUPLE
print(fruits)

for fruit in fruits:  # Second Example
    print('TUPLE fruit :', fruit)

fruits = ['banana', 'apple', 'mango']
print(len(fruits))
for index in range(len(fruits)):
    print('Current fruit :', fruits[index])

for num in range(10, 20):  # to iterate between 10 to 20
    for i in range(2, num):  # to iterate on the factors of the number
        if num % i == 0:  # to determine the first factor
            j = num / i  # to calculate the second factor
            print('%d equals %d * %d' % (num, i, j))
            break  # to move to the next number, the #first FOR
        else:  # else part of the loop
            print(num, 'is a prime number')

i = 2
while(i < 100):
    j = 2
    while(j <= (i / j)):
        if not(i % j): break
        j = j + 1
        if (j > i / j) : print(i, " is prime")
        i = i + 1
         
print("Good bye!")

for letter in 'Python':  # First Example
    if letter == 'h':
        break
    print('Current Letter :', letter)
  
var = 10  # Second Example
while var > 0:              
    print('Current variable value :', var)
    var = var - 1
    if var == 5:
        break

for letter in 'Python':  # First Example
    if letter == 'h':
        continue
    print('Current Letter :', letter)

var = 10  # Second Example
while var > 0:              
    var = var - 1
    if var == 5:
        continue
    print('Current variable value :', var)

# PASS - The pass statement is a null operation; nothing happens when it executes.
for letter in 'Python': 
    if letter == 'h':
        pass
    print('This is pass block')
    print('Current Letter :', letter)
