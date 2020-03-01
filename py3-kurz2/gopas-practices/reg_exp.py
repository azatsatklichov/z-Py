'''
Regular expressions
• Complex searching and substitutions
• Regular expression is not specially quoted in Python
• Be careful on \
• Use raw string r”\\.html$”
• Anchors ^,$
• Quantifiers *+? {}
• Character sets [] [^], interval a-z
• \\d \\w \\z
• Grouping () \\1..\\99

import re
• Compilation re.compile(re,[modifiers])
• Methods of object representing RE
• match
• search
• findall
• finditer
• Or you can use match(re,string), search(re,string)…

Match object
• Methods
• start()
• end()
• group()
• span()
• Named group (?P<name>…)
• m=re.compile("a+")
• s="accaabaaavvv”
• print m.findall(s) #['a', 'aa', 'aaa']

Substitution with RE
• Methods of object representing RE
• split(string[, maxsplit=0])
• sub(replacement, string[, count=0])
• subn(replacement, string[, count=0])
• m=re.compile("a+")
• s="accaabaaavvv”
• print m.sub('A',s) #AccAbAvvv
'''

import re

print()
line = "Cats are smarter than dogs"

matchObj = re.match( r'(.*) are (.*?) .*', line, re.M|re.I)

if matchObj:
   print("matchObj.group() : ", matchObj.group())
   print("matchObj.group(1) : ", matchObj.group(1))
   print("matchObj.group(2) : ", matchObj.group(2))
else:
   print("No match!!")


print()
print()

line = "Cats are smarter than dogs";

searchObj = re.search( r'(.*) are (.*?) .*', line, re.M|re.I)

if searchObj:
   print("searchObj.group() : ", searchObj.group())
   print("searchObj.group(1) : ", searchObj.group(1))
   print("searchObj.group(2) : ", searchObj.group(2))
else:
   print("Nothing found!!")


print()
print()
line = "Cats are smarter than dogs";
matchObj = re.match( r'dogs', line, re.M|re.I)
if matchObj:
   print("match --> matchObj.group() : ", matchObj.group())
else:
   print("No match!!")

searchObj = re.search( r'dogs', line, re.M|re.I)
if searchObj:
   print("search --> searchObj.group() : ", searchObj.group())
else:
   print("Nothing found!!")


print()
print()
phone = "2004-959-559 # This is Phone Number"
# Delete Python-style comments
num = re.sub(r'#.*$', "", phone)
print("Phone Num : ", num)

# Remove anything other than digits
num = re.sub(r'\D', "", phone)    
print("Phone Num : ", num)

print()
print()

