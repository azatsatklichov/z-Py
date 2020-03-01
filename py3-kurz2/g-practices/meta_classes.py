'''
Metaclasses

	A metaclass is to a class what a class is to an instance; that is, a
metaclass is used to create classes, just as classes are used to create
instances. And just as we can ask whether an instance belongs to a
class by using isinstance(), we can ask whether a class object (such as
dict, int, or SortedList) inherits another class using issubclass().

 	One use of metaclasses is to provide both a promise and a guarantee
about a class’s API. Another use is to modify a class in some way (like
a class decorator does). And of course, metaclasses can be used for
both purposes at the same time.
'''
class A:

a = A()

isinstance(a, A) #True
isinstance(b, A) #False
isinstance(b, B) #True
isinstance(b, A) #False

isinstance(A, type) #True
isinstance(a, type) #False
isinstance(B, type) #True
isinstance(b, type) #False


#inheritance
print("https://www.python-course.eu/python3_multiple_inheritance.php")
print("MRO - method resolution order")
