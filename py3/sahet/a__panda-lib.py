#Pandas is a Python library.
#Pandas is used to analyze data.

#https://www.w3schools.com/python/pandas/default.asp

import pandas

mydataset = {
  'cars': ["BMW", "Volvo", "Ford"],
  'passings': [3, 7, 2]
}

myvar = pandas.DataFrame(mydataset)

print(myvar)