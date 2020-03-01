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

class firstn(object):
  def __init__(self, n):
    self.n = n
    self.num= 0
  def __iter__(self):
    return self

  # Python 3 compatibility
  def __next__(self):
    return self.next()
  def next(self):
    if self.num< self.n:
      cur, self.num= self.num, self.num+1
      return cur
    else:
      raise StopIteration()

first_n = firstn(100)
print(first_n)
for i in first_n:
  print(i, end=', ')

sum_of_first_n = sum(firstn(100))

