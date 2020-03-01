

print("Diamond issue - http://www.aizac.info/a-solution-to-the-diamond-problem-in-python/")

print("C3 linearization - https://en.wikipedia.org/wiki/C3_linearization")

class A:
  def call(self):
    pass
 
class B1(A):
  def call(self):
    print "I am parent B1"
 
class B2(A):
  def call(self):
    print "I am parent B2"
 
class B3(A):
  def call(self):
    print "I am parent B3"
 
class C(A):
  def call(self):
    print "I (C) was not invited"
 
class ME(B2, B1, B3):
  def whichCall(self):
    print self.call()
 
  def restructure(self, parent1, parent2, parent3):
    self.__class__.__bases__ = (parent1, parent2, parent3, )
 
  def printBaseClasses(self):
  	print self.__class__.__bases__
