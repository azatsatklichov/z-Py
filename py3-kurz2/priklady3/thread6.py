from multiprocessing import Process, Lock, Value
import time
def f(l, x):
  l.acquire()
  x.value += 1
  time.sleep(5)
  print(x.value)
  l.release()

if __name__ == '__main__':
  lock = Lock()
  n = Value('d', 0)
  sez = list()
  for i in range(10):
    sez.append(Process(target=f, args=(lock, n)))
    sez[i].start()

  for i in range(10):
    sez[i].join()
    print("Vysledna hodnota n:", n.value)

