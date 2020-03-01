class B():
  def __call__(self,x):
    pass

class A():
  def __init__(self,jm):
    self.__jmeno=B()
  @property
  def Jmeno(self):
    return self.__jmeno
  @Jmeno.setter
  def Jmeno(self,nove):
    self.__jmeno=nove

a=A('Pepa')
#print(a.Jmeno)
#a.Jmeno="Josef"
#print(a.Jmeno)
a.Jmeno('Josef')
