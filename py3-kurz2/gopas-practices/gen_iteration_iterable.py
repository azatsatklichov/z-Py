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

