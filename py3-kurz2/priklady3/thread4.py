import os
from multiprocessing import Process 
import time
def f():
  print(os.getpid(), ": zacatek...")
  time.sleep(os.getpid() % 7)
  print(os.getpid(), ": trvalo mi to", (os.getpid() % 7), "s.")

if __name__ == '__main__':
  for i in range(7):
    p = Process(target=f, args=())
    p.start()
