
#import urllib     - ishlanok 
import urllib.request as urllib
try:
	#seznam=urllib.urlopen("http://www.seznam.cz/")
	#fl=urllib.urlopen("http://127.0.0.1:5000/web_programming-flaskpy.py ")
	fl=urllib.urlopen("http://127.0.0.1:5000/")
	try:
		for radek in fl.readlines():
			print (radek.strip())
	finally:
		fl.close()
except:
	print("Chyba !!!!")
	