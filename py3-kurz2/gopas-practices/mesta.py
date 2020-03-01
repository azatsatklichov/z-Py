mesta={}	
soubor=open("mesta.txt")
for radek in soubor.readline():
	radek=radek.strip()
	kod,mesto=radek.split(',',1)
	if kod in mesta:
		mesta[kod].append(mesto)
	else:
		mesta[kod]=[mesto]
for kod in sorted(mesta.keys()):
	mesta[kod].sort()
	print(kod, ":", ','.join(mesta[kod]))
