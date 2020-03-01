def f():
	a=10
	def f1():
		nonlocal a
		print(a)
		a+=1
	f1()
	return f1


x=f()
x=f()
x=f()

print()
print("how to call")
x=f()
x()
x()

