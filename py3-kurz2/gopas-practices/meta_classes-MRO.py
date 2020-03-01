#inheritance
print("https://www.python-course.eu/python3_multiple_inheritance.php")
print("MRO - method resolution order")

class A():
	def fce(self):
		print("Trida A")

class B():
	def fce(self):
		print("Trida B")


class C(A):
	#pass
	def fce(self):
		print("Trida C")


class D(B):
	#pass
	def fce(self):
		print("Trida D")

class E(C, D):
	def fce(self):
		print("Trida E")

x=E()
print(x.fce())

print("Diamond issue - http://www.aizac.info/a-solution-to-the-diamond-problem-in-python/")

print("C3 linearization - https://en.wikipedia.org/wiki/C3_linearization")