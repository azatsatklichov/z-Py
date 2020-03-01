'''
Created on Jan 7, 2018

@author: satklichov
'''
list1 = ['physics', 'chemistry', 1997, 2000];
list2 = [1, 2, 3, 4, 5, 6, 7 ];
print ("list1[0]: ", list1[0])
print ("list2[1:5]: ", list2[1:5])


#delete
list1 = ['physics', 'chemistry', 1997, 2000];
print (list1)
del list1[2];
print ("After deleting value at index 2 : ")
print (list1)

list1, list2 = ['123', 'xyz', 'zara', 'abc'], [456, 700, 200]
xx =min(list1)
print(xx) 

aList = [123, 'xyz', 'zara', 'abc']
aList.insert( 3, 2009)
print ("Final List : ", aList)

aList = [123, 'xyz', 'zara', 'abc'];
print (aList)
print ("A List : ", aList.pop())
print (aList)
print ("B List : ", aList.pop(2))


print()

aList = [123, 'xyz', 'zara', 'abc', 'xyz'];
aList.remove('xyz');
print (aList)
aList.remove('abc');
print (aList)


print()


aList = [123, 'xyz', 'zara', 'abc', 'xyz'];
aList.reverse();
print (aList)

print()
aList = ['123', 'xyz', 'zara', 'abc', 'xyz'];
aList.sort();
print (aList)

