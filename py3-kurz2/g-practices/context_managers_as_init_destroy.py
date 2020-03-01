'''
Context Managers
• with object1 [as name1][, object2 [as name2]] ...:
• [indented suite]
• The Context Manager Protocol: __enter__() and __exit__()
• The with statement has rules for interacting with the object it is given as a
context manager. It processes with expr by evaluating the expression and
saving the resulting context manager object. The context manager's
__enter__() method is then called, and if the as name clause is included,
the result of the method call is bound to the given name. Without the as
name clause, the result of the __enter__() method is not available. The
	indented suite is then executed.
	'''
#like Java/Spring
#init, destroy

#see mesto5.py