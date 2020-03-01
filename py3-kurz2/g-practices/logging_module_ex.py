'''
logging module
• Logging module to log errors and debugging messages
• Provides central control over debugging output

LEVEL
logging.basicConfig(level=logging.LEVEL)
--------
CRITICAL, logging.critical()
ERROR, logging.error()
WARNING, logging.warning()
INFO,logging.info()
DEBUG, logging.debug()


logging
• Can output messages to a log file
• logging.basicConfig(level=logging.DEBUG, filename = ‘bugs.log’)

• Can add time
• logging.basicConfig(level=logging.DEBUG, filename=‘bugs.log’,
format=‘%(asctime)s %(message)’)
'''
 
import logging
logging.basicConfig(level = logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s') 
logging.debug('start programming')
def mirror(lst):
	ret = []
	for i in range(len(lst)):
		ret.append(lst[-i - 1])
		logging.error("list for i={0}: {1} ".format(i, lst[-i - 1]))
	return lst + ret

mirror([23,-4,4,4,3])

#import syslog
#dir(syslog)
import os
logging.info(print())
logging.info(dir(os))



