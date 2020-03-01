#!/usr/bin/env python3.6
import time
import regex as re
import logging
class Stat:
  def __init__(self,kod_statu,mesto=""):
    self.kod=kod_statu
    self.mesta=[]
    if mesto!="":
      self.mesta.append(mesto)
  def pridej(self,mesto):
    self.mesta.append(mesto)
  def vypis(self):
    #self.mesta.sort()
    print(self.kod,":",','.join(sorted(self.mesta)))
  def __add__(self,other):
    if isinstance(other,str):
      self.mesta.append(other)
      return self
    elif isinstance(other,Stat):
      novy=Stat(self.kod+other.kod)
      novy.mesta=self.mesta+other.mesta
      return novy
    else:
      raise TypeError
  def __str__(self):
    return ','.join(self.mesta)

def timeit(fce):
  def obal():
    t1=time.time()
    fce()
    t2=time.time()
    print("Volani trvalo : {}".format(str(t2-t1)))
  return obal

#@timeit
def hlavni():
  logging.basicConfig(level = logging.WARN,format='%(asctime)s %(message)s')
  staty={}
  #regex=re.compile('^([A-Z]{2}),(.+)')
  regex=re.compile('^([[:upper:]]{2}),([[:alpha:]]+(?: [[:alpha:]]+)*)')
  try:
    with open("mesta.txt") as soubor:
      for radek in soubor:
        m=regex.search(radek)
        if m:
          kod,mesto=m.groups()
          if kod in staty:
            staty[kod]+=mesto
          else:
            staty[kod]=Stat(kod,mesto)
        else:
          logging.error("Chybny radek: "+radek.rstrip())
  except IOError as chyba:
    print("Nastala chyba:",chyba)
  staty["CZ"].pridej("Kladno")
  for kod in sorted(staty.keys()):
    staty[kod].vypis()
  print("Serazeny vypis mest pro CZ+SK")
  Novy=staty['CZ']+staty['SK']
  #chybny radek Novy=staty['CZ']+123
  Novy.vypis()

if __name__=="__main__":
  hlavni()
