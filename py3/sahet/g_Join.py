

s = "-";
seq = ("a", "b", "c"); # This is sequence of strings.
print (s.join( seq ))


seq = ("a", "b", "c"); # This is sequence of strings.
print (s.join( seq))

_str = "this is string example....wow!!!";
print (_str.ljust(50, '0'))
print (_str.rjust(100, '0'))

_str = "     this is string example....wow!!!     ";
print (_str.rstrip())
_str = "88888888this is string example....wow!!!8888888";
print (_str.rstrip('8'))



_str = "     this is string example....wow!!!     ";
print (_str.lstrip())
_str = "88888888this is string example....wow!!!8888888";
print (_str.lstrip('8'))

_str = "0000000this is string example....wow!!!0000000";
print (_str.strip( '0' ))


_str = "Line1-a b c d e f\nLine2- a b c\n\nLine4- a b c d";
print (_str.splitlines( ))
print (_str.splitlines( 0 ))
print (_str.splitlines( 3 ))
print (_str.splitlines( 4 ))
print (_str.splitlines( 5 ))

_str = "this is string example....wow!!!";
print ("_str.capitalize() : ", _str.upper())