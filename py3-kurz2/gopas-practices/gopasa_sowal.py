'''
List Comprehensions is a very powerful tool, which creates a new list based on another list, in a single, readable line.
For example, let's say we need to create a list of integers which specify the length of each word in a certain sentence, but only if the word is not the word "the".
'''
sentence = "the quick brown fox jumps over the lazy dog"
words = sentence.split()
word_lengths = []
for word in words:
	if word != "the":
		word_lengths.append(len(word))

print(words)
words = sentence.split()
word_lengths = [len(wrd) for wrd in words if wrd != "jumps"]
print(word_lengths)
print()
#Actually this is a FUNCTION call
word_l = [wrd for wrd in words if wrd != "the"]
print(word_l)

print()
 

# ERR
# word_lengths = [for wrd in words if wrd != "the"]
# Using a list comprehension, create a new list called "newlist" out of
# the list "numbers", which contains only the positive numbers from the
# list, as integers

numbers = [34.6, -203.4, 44.9, 68.3, -12.2, 44.6, 12.7]
newlist = []
for n in numbers:
	if n > 0:
		newlist.append(n)

print(newlist)

#other way around
newlist = [n*2 for n in numbers if n>0]
print(newlist)




