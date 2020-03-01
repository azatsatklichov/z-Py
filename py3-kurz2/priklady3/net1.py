import urllib
try:
  seznam=urllib.urlopen("http://www.seznam.cz/")
  try:
    for radek in seznam.readlines():
      print (radek.strip())
  finally:
    seznam.close()
except:
  print("Chyba !!!!")
