#!/usr/bin/env python3.6
class Stat:

  def __init__(self, kod_statu, mesto=""):
    self.kod = kod_statu
    self.mesta = []
    if mesto != "":
      self.mesta.append(mesto)

  def pridej(self, mesto):
    self.mesta.append(mesto)

  def vypis(self):
    # self.mesta.sort()
    print(self.kod, ":", ','.join(sorted(self.mesta)))

  def __add__(self, other):
    if isinstance(other, str):
      self.mesta.append(other)
      return self
    elif isinstance(other, Stat):
      novy = Stat(self.kod + other.kod)
      novy.mesta = self.mesta + other.mesta
      return novy
    else:
      raise TypeError

  def __str__(self):
    return ','.join(self.mesta)


staty = {}
try:
  with open("mesta.txt") as soubor:
    for radek in soubor:
      kod, mesto = radek.rstrip().split(',', 1)
      if kod in staty:
        staty[kod] += mesto
        # staty[kod].pridej(mesto)
      else:
        staty[kod] = Stat(kod, mesto)
except IOError as chyba:
  print("Nastala chyba:", chyba)
staty["CZ"].pridej("Kladno")
for kod in sorted(staty.keys()):
  staty[kod].vypis()
print("Serazeny vypis mest pro CZ+SK")
Novy = staty['CZ'] + staty['SK']
# chybny radek Novy=staty['CZ']+123
Novy.vypis()
