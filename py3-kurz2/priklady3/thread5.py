import os
from multiprocessing import Process, Lock
import time
def f(l):
  print(os.getpid(), ": zacatek ...")
  l.acquire()
  time.sleep(os.getpid() % 7)
  l.release()
  print(os.getpid(), ": trvalo mi to", (os.getpid() % 7), "s.")

if __name__ == '__main__':
  lock = Lock()
  for i in range(7):
    Process(target=f, args=(lock,)).start()

