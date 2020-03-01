'''
Coroutines
• Coroutines are functions whose processing can be suspended and
resumed at specific points. So, typically, a coroutine will execute up to
a certain statement, then suspend execution while waiting for some
data. At this point other parts of the program can continue to execute
(usually other coroutines that aren’t suspended).
'''

#import coroutines
#from coroutines import finditer, send
#import types 
from types import coroutine
#Coroutines
@coroutine
def regex_matcher(receiver, regex):
	while True:
		text = (yield)
		for match in regex.finditer(text):
			receiver.send(match)




