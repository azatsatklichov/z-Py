class firstn(object):

  def __init__(self, n):
    self.n = n
    self.num = 0

  def __iter__(self):
    return self

  # Python 3 compatibility
  def __next__(self):
    return self.next()

  def next(self):
    if self.num < self.n:
      cur, self.num = self.num, self.num + 1
      return cur
    else:
      raise StopIteration()


y = firstn(20)
for i in y:
  print(i)
print(sum(firstn(500)))
s = set(firstn(10))
print(s)
