def f(a, L=[]):
  """Toto je funkce s jednim povinnym a jednim volitelnym parametrem
  Zajimava je inicializace"""
  L.append(a)
  return L
print(f(10))
print(f(20))
print(f(30))
#print(f.__doc__)

def f(a, L=None):
  """Toto je funkce s jednim povinnym a jednim volitelnym parametrem
  Zajimava je inicializace"""
  if L is None:
    L=[]
  L.append(a)
  return L
print(f(10))
print(f(20))
print(f(30))
