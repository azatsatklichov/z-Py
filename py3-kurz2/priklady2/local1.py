def f():
  print(a)
  b = 20
  print(b)


# f() - NameError: name 'a' is not defined
a = 1
b = 2
f()
print(a, b)
