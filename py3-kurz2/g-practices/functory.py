
'''
Functor is simply a mapping fromone type of data to another.
• In Python a function object is an object reference to any callable, such
as a function, a lambda function, or a method. The definition also
includes classes, since an object reference to a class is a callable that,
when called, returns an object of the given class—for example, x =
int(5). 

In computer science a functor is an object that can be called as
though it were a function, 

so in Python terms a functor is just another
kind of function object. 

Any class that has a __call__() special method
	is a functor.

https://docs.python.org/3/index.html

Built-in methods
https://docs.python.org/3/library/functions.html?highlight=staticmethod

'''

#callable objects

class A():
	def __call__(self):
		print("Volas me jako funkci")

a=A()
print(a)
#PERFECT
a()

b=a
type(b)
print(b)

print("----")
b=a()

