class Person:
	def __init__(self,name,age):
		self.name=name
		self.age=age

	def __str__(self):
		return(self.name)

	def __gt__(self,other):
		if (self.age>other.age):
			return True
		return False

	def __add__(self,other):
		return self.age+other.age

	def printall(self):
		print("Name : %s, age : %d" % (self.name,self.age))

print("not so practical with sublime")
bob=Person("Bob",20)
alice=Person("Alice",19)
print(bob+alice)


