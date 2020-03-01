
#import urllib     - ishlanok 
import urllib.request as urllib
try:
	#seznam=urllib.urlopen("http://www.seznam.cz/")
	sahet=urllib.urlopen("http://www.sahet.net")
	try:
		for radek in sahet.readlines():
			print (radek.strip())
	finally:
		sahet.close()
except:
	print("Chyba !!!!")
	