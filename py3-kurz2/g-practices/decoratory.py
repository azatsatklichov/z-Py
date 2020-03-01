class Person:
	Person_id=1
	def __init__(self,name,age):
		self.name=name
		self.age=age
		self.cid=Person.Person_id
		Person.Person_id+=1
	

	def __str__(self):
		return(self.name)

	'''
	A decorator is the name used for a software design pattern.
	Decorators dynamically alter the functionality of a function, method,
	or class without having to directly use subclasses or change the
	source code of the function being decorated
	'''	
	@classmethod
	def resetPerson(cls):
		cls.Person_id=1

	def printall(self):
		print ("Name : %s, age : %d, id : %d" % (self.name,self.age,self.cid))


p =Person("Azat", 41)
print(p)
p.resetPerson()


