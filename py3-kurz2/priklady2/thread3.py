import os
from multiprocessing import Process
def info(title):
  print(title)
  print('module name: '+ __name__)
  print('parent process: '+ str(os.getppid()))
  print('process id: '+ str(os.getpid()))
  print('')
def f(name):
  info('> function f')
  print('hello', name)

if __name__ == '__main__':
  info('> main line')
  p = Process(target=f, args=('bob',))
  p.start()
  #p.join()
  print "End >main line"
