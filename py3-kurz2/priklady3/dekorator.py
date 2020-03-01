def pozdrav_me(jmeno):
	return "Ahoj "+jmeno

def dekorator_pozdravu(funkce_pozdravu):
	def obal(jmeno):
		return "<b>%s</b>"%(funkce_pozdravu(jmeno))
	return obal

vyvolej_pozdrav=dekorator_pozdravu(pozdrav_me)

print(vyvolej_pozdrav('Jardo'))

pozdrav_me=dekorator_pozdravu(pozdrav_me)

print(pozdrav_me('Jardo'))

###############################################
#a ted to udelame pres dekorator

def dekorator_pozdravu(funkce_pozdravu):
        def obal(jmeno):
                return "<b>%s</b>"%(funkce_pozdravu(jmeno))
        return obal

@dekorator_pozdravu
def pozdrav_me(jmeno):
        return "Ahoj "+jmeno

print(pozdrav_me('Honzo'))
