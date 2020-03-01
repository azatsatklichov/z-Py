class Person2:

	Person_id=1

	def __init__(self,name,age):
		self.name=name
		self.age=age
		self.cid=Person2.Person_id
		Person2.Person_id+=1


	def __str__(self):
		return(self.name)

	def __gt__(self,other):
		if (self.age>other.age):
			return True
		return False

	def __add__(self,other):
		return self.age+other.age

	def printall(self):
		print("Name : %s, age : %d, id: %d" % (self.name,self.age, self.cid))

	#cls --> self
	def resetPerson(cls):
		cls.Person_id=1


print("not so practical with sublime")
bob=Person2("Bob",20)
alice=Person2("Alice",19)
print(bob+alice)
bob.printall()
alice.printall()

#to String method
print(bob)
print(alice)

print("\n  -- -type - --")
print(type(bob))
x =123
print(type(x))


print()
print("-- reset person --")
bob2=Person2("Bob",20)
alice2=Person2("Alice",19)
print(bob2)
print(alice2)
alice2.resetPerson()
lor2=Person2("Bob",20)
lor2.printall()




