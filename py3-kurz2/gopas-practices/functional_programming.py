'''
Functional style programming
• Functional programming are these concepts: mapping, filtering, and
reducing
• list(map(lambda x: x ** 2, [1, 2, 3, 4]))
• [x ** 2 for x in [1, 2, 3, 4]]
• list(filter(lambda x: x > 0, [1, -2, 3, -4]))
• [x for x in [1, -2, 3, -4] if x > 0]


Functional style programming
• functools.reduce(lambda x, y: x * y, [1, 2, 3, 4])
• functools.reduce(operator.mul, [1, 2, 3, 4])
• functools.reduce(operator.add, (os.path.getsize(x) for x in files))
• functools.reduce(operator.add, map(os.path.getsize, files))

'''

s = lambda x: "" if x==1 else "s"
print(s)
print(s(4))


print(list(map(lambda x: x**2, [1,2,3,4])))


def moje(x):
	return x**2

print(list(map(moje, [1,2,3,4])))


#or generating LISt dynamically
x = [x**2 for x in [2,4,6,8,9]]
print(x)


y  = [x for x in [1, -2, 3, -4] if x > 0]
print(y)


print("\n   reduce ")
import functools


print("\n   comprehensive  - flattening list")

ll = [x for sublist  x in [[1,2,3], [5,7,8], [10, 11]]]
print(ll) 


kk  = [[1,2,3], [5,7,8], [10, 11]]
comrh = []
for k in kk:
	ar = kk[k]
	for t in ar:
		v = ar[t]
		comrh.append(v)

print(comrh)

ll = [x for x in [[1,2,3], [5,7,8], [10, 11]]]
print(ll)  


