class A():

  def __init__(self, jm):
    self.__jmeno = jm

  @property
  def Jmeno(self):
    return self.__jmeno

  @Jmeno.setter
  def Jmeno(self, nove):
    self.__jmeno = nove


a = A('Pepa')
print(a.Jmeno)
a.Jmeno = "Josef"
print(a.Jmeno)
