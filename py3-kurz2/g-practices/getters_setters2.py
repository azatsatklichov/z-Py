
class Person (object):
	def __init__(self,name,age):
		self.__name=name
		self.__age=age

	def printit(self):
		print ("Name is : %s, age is : %d" % (self.__name,self.__age))

	@property
	def name(self):
		return self.__name
	
	@name.setter
	def name(self,name):
		self.__name=name
	
#TypeError: 'str' object is not callable
print("----- TypeError: 'str' object is not callable ------")
bob2=Person("Bob",20)
print("-->"+ bob2.name)
print("Normal SET is not working ")
bob2.name("PYTHON")
print(bob2.name)

