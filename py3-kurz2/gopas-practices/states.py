class Stat:
	def __init__(self, kod, mesto):
		self.kod=kod
		self.mesto=[mesto]

	def pridej(self, mesto):
		self.mesto.append(mesto)

	def vypis(self):
		#self.mesta.sort()
		print(self.kod, ":", ','.join(sorted(self.mesto)))

staty={}
try:
	with open("mesta.txt") as soubor:
		for radek in soubor:
			kod,mesto=radek.rstrip().split(',', 1)
			if kod in staty:
				staty[kod]+=mesto
			else:
				staty[kod]=Stat(kod,mesto)
except IOError as chyba:
	print("Nastala chyba: ", chyba)
for kod in sorted(staty.keys()):
	staty[kod].vypis



