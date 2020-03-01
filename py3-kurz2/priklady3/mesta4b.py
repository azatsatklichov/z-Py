#!/usr/bin/env python3.6
class Stat:
  def __init__(self,kod_statu,mesto=""):
    self.__kod=kod_statu
    self.__mesta=[]
    if mesto!="":
      self.__mesta.append(mesto)
  def pridej(self,mesto):
    self.__mesta.append(mesto)
  def vypis(self):
    #self.mesta.sort()
    print(self.__kod,":",','.join(sorted(self.__mesta)))
  def __add__(self,other):
    if isinstance(other,str):
      self.__mesta.append(other)
      return self
    elif isinstance(other,Stat):
      novy=Stat(self.__kod+other.__kod)
      novy.__mesta=self.__mesta+other.__mesta
      return novy
    else:
      raise TypeError
  def __str__(self):
    return ','.join(self.__mesta)

staty={}
try:
  with open("mesta.txt") as soubor:
    for radek in soubor:
      kod,mesto=radek.rstrip().split(',',1)
      if kod in staty:
        staty[kod]+=mesto
        #staty[kod].pridej(mesto) 
      else:
        staty[kod]=Stat(kod,mesto)
except IOError as chyba:
  print("Nastala chyba:",chyba)
staty["CZ"].pridej("Kladno")
for kod in sorted(staty.keys()):
  staty[kod].vypis()
print("Serazeny vypis mest pro CZ+SK")
Novy=staty['CZ']+staty['SK']
Novy.vypis()
