def f(ham: str, eggs: str = 'Eggs') -> str:
  print("Annotations:", f.__annotations__)
  print("Arguments:", ham, eggs)
  return str(ham) + ' and ' + eggs

print(f('HAM'))
print(f('HAM','EGGS'))
print(f('HAM',eggs='EGGS'))
print(f(123))
