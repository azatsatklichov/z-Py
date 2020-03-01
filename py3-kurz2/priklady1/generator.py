def firstn(n):
  num = 0
  while num < n:
    yield num
    num += 1

sum_of_first_n = sum(firstn(100))
print(sum_of_first_n)
print(firstn(10))
for i in firstn(10):
  print(i)
