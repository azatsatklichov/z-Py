import mmap
with open("pokus.txt","r+b") as f:
  mapf=mmap.mmap(f.fileno(),0)
  print(mapf[:].decode())
  print(mapf[:5].decode())
  mapf[0:6]=b'WO2345'
  mapf[0:1]=b'X'
  mapf.seek(4)
  print(mapf.readline())
  print(mapf.tell())
  print(mapf[:].decode())
  
