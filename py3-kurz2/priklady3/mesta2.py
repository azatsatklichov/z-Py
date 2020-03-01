#!/usr/bin/env python3.3
mesta={}
try:
  with open("mesta.txt") as soubor:
    for radek in soubor:
      radek=radek.strip()
      kod,mesto=radek.split(',',1)
      if kod in mesta:
        mesta[kod].append(mesto)
      else:
        mesta[kod]=[mesto]
except IOError as chyba:
  print("Nastala chyba:",chyba)
for kod in sorted(mesta.keys()):
  mesta[kod].sort()
  print(kod,":",','.join(mesta[kod]))

