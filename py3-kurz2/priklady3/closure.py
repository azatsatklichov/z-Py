def f():
  a=10
  def f1():
    nonlocal a
    print(a)
    a+=1
  f1()
  return f1

x=f()
x()
print(type(x.__closure__[0].cell_contents))
x()
x=f()
x()
x()
