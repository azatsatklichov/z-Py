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

bob=Person("Bob",20) 
print(bob.name)
bob.name="BOB"
print(bob.name)
