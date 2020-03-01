'''
Created on Jan 7, 2018

@author: satklichov

'''

print("ahemmesi gowuluga bolar insalla")

_str = "this is string example....wow!!!";
print ("_str.center(40, 'a') : ", _str.center(40, 'a'))



_str = "this is string example....wow!!!";
print (_str.isdigit())


_str = "this is string example....wow!!!";

suffix = "wow!!!";
dx =  _str.endswith(suffix) 
print(dx)

sub = "i";
print ("_str.count(sub, 4, 40) : ", _str.count(sub, 4, 40))
sub = "wow";
print ("_str.count(sub) : ", _str.count(sub))

Str = "this is string example....wow!!!";
Str = Str.encode('base64','strict');

print ("Encoded String: " + Str)
print ("Decoded String: " + Str.decode('base64','strict'))
