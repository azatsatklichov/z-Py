class A():
  def __init__(self,r=True):
    self.r=r
    print("Novy Context Manager vytvoren")
  def __enter__(self):
    print("Volana metoda __enter__")
    return self
  def __exit__(self,exc_type,exc_val,exc_tb):
    print("Exit z Context Manageru")
    if exc_type:
      print("Nastala chyba")
      if self.r:
        print("Preposilame chybu vyse")
      return not self.r

with A() as neco:
  print("Context manager",neco)
  x=10/0
  print("Po chybe")

