'''
Iterable/Iterator
  Iterable is everything what can be used to iterate over:
  for var in iterable:
  for i in ‘cau’: print i
  Iterator is object which remembers state where is during and between
iteration calls
  s=“Bye”
  i=iter(s)
  next(i) #‘B’
  next(i) #‘y’
  next(i) #’e’
  next(i) #exception StopIteration

  '''

def firstn(n):
	num = 0
	while num < n:
		yield num
		num += 1

sum_of_first_n = sum(firstn(100))
print(sum_of_first_n)

for i in firstn(10):
  print(i,end =', ')

