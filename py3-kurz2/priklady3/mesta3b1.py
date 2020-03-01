#!/usr/bin/env python3.6
class Stat:
  def __init__(self,kod_statu,mesto):
    self.__kod=kod_statu
    self.__mesta=[mesto]
  def pridej(self,mesto):
    self.__mesta.append(mesto)
  def vypis(self):
    #self.__mesta.sort()
    print(self.__kod,":",','.join(sorted(self.__mesta)))
  def __add__(self,other):
    self.pridej(other)
    return self

staty={}
try:
  with open("mesta.txt") as soubor:
    for radek in soubor:
      kod,mesto=radek.rstrip().split(',',1)
      if kod in staty:
        staty[kod]+=mesto
      else:
        staty[kod]=Stat(kod,mesto)
except IOError as chyba:
  print("Nastala chyba:",chyba)
for kod in sorted(staty.keys()):
  staty[kod].vypis()
print(staty["CZ"]+staty["SK"])
