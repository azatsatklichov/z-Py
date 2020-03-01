class Mnesto:

    def __init__(self, name, code):
        self.name = name
        self.code = code
        self.description = "City desc"

    def describe(self, name):
        self.name = name

    def cityName(self, name):
        self.name = name

    def __str__(self, name):
     return name 


p = Mnesto("Praha", "cz")
b = Mnesto("Bratislava", "sk")
m = Mnesto("Moscow", "ru")

#print(p.name)

#list of cities
ls  = [p, b, m]
for city in ls:
	print(city.name)

#ls.sort()
#print(ls.sort())

nm = [3, 56,6,-7,77]
#print(nm.sort())
print(nm)
nm.sort()
print(nm)



