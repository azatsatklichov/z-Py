class A():
  pass
  def fce(self):
    print("Trida A")
class B():
  def fce(self):
    print("Trida B")
class C(A):
  pass
  #def fce(self):
  #  print("Trida C")
class D(B):
  pass
  def fce(self):
    print("Trida D")
class E(C,D):
  pass
#  def fce(self):
#    print("Trida E")
x=E()
x.fce()
try:
  print(E.mro())
except:
  pass
