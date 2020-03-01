''' 
'''
import os
dir(os)


print(eval('12+3'))

#
x = compile("print(123)", "<string>", 'exec')
exec(x)

#
eval(compile("print(123)", "<string>", 'exec'))


#mmap - bytearray
print("\n   mmap - bytearray")
x=b'hello\n'
print(x)
print(x[1])
type(x) 

s = str(x)
print(s)

s=str(x, 'utf-8')
print(s)
print('--string from byte array')
s=x.decode()
print(s)





