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

class ctx_mgr:
	def __init__(self, raising=True):
		print("Create new context ")
		self.raising = raising
	
	def __enter__(self):
		print("Enter called")
		cm = object()
		print("__enter__ returning object id:"+id(cm))
		return cm


	def __exit__(self, ext_type, exc_val, exc_tb):
		print("__exit__ called")
		if ext_type:
			print("Exception occured")
			if self.raising:
				print("Raising exception")
			return not self.raising

with ctx_mgr(raising=True)as cm:
	print("cm ID: ", id(cm))

