#!/usr/bin/env python3.6
class Stat:

  def __init__(self, kod_statu, mesto):
    self.kod = kod_statu
    self.mesta = [mesto]

  def pridej(self, mesto):
    self.mesta.append(mesto)

  def vypis(self):
    # self.mesta.sort()
    print(self.kod, ":", ','.join(sorted(self.mesta)))


staty = {}
try:
  with open("mesta.txt") as soubor:
    for radek in soubor:
      kod, mesto = radek.rstrip().split(',', 1)
      if kod in staty:
        staty[kod].pridej(mesto)
      else:
        staty[kod] = Stat(kod, mesto)
except IOError as chyba:
  print("Nastala chyba:", chyba)
for kod in sorted(staty.keys()):
  staty[kod].vypis()

