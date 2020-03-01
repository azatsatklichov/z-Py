def f():
  global a
  a = 10
  print(a)
  b = 20
  print(b)


a = 1
b = 2
f()
print(a, b)
