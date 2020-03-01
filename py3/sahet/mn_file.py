
# Open a file
fo = open("foo.txt", "r+")
_str = fo.read(50);
print ("Read String is : ", _str)

# Check current position
position = fo.tell();
print ("Current file position : ", position)

# Reposition pointer at the beginning once again
position = fo.seek(0, 0);
_str = fo.read(10);
print ("Again read String is : ", _str)
# Close opend file
fo.close()