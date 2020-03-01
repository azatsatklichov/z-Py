'''
Created on Jan 7, 2018

@author: satklichov

The standard library comes with a number of modules that can be 
used both as modules and as command-line utilities.
'''

# The dis module is the Python disassembler.
# It converts byte codes to a format that is slightly more appropriate for human consumption.
import dis

print ("\n\nDIS - disaassembler")
def sum():
   vara = 10
   varb = 20

   sum = vara + varb
   print ("vara + varb = %d" % sum)

# Call dis function for the function.

dis.dis(sum)


#The pdb module is the standard Python debugger. It is based on the bdb debugger framework.
print ("\n\nPDB - py debugger")
'''
SEE:C:\python364\Lib,    pdb.py file there


$pdb.py sum.py
> /test/sum.py(3)<module>()
-> import dis
(Pdb) n
> /test/sum.py(5)<module>()
-> def sum():
(Pdb) n
>/test/sum.py(14)<module>()
-> dis.dis(sum)
(Pdb) n
  6           0 LOAD_CONST               1 (10)
              3 STORE_FAST               0 (vara)

  7           6 LOAD_CONST               2 (20)
              9 STORE_FAST               1 (varb)

  9          12 LOAD_FAST                0 (vara)
             15 LOAD_FAST                1 (varb)
             18 BINARY_ADD
             19 STORE_FAST               2 (sum)

 10          22 LOAD_CONST               3 ('vara + varb = %d')
             25 LOAD_FAST                2 (sum)
             28 BINARY_MODULO
             29 PRINT_ITEM
             30 PRINT_NEWLINE
             31 LOAD_CONST               0 (None)
             34 RETURN_VALUE
--Return--
> /test/sum.py(14)<module>()->None
-v dis.dis(sum)
(Pdb) n
--Return--
> <string>(1)<module>()->None
(Pdb)
'''


print ("\n\nprofile - The profile module is the standard Python profiler.")
'''
Now, try running cProfile.py over this file sum.py as follows −

$cProfile.py sum.py
vara + varb = 30
         4 function calls in 0.000 CPU seconds

   Ordered by: standard name

ncalls  tottime  percall  cumtime  percall filename:lineno
   1    0.000    0.000    0.000    0.000 <string>:1(<module>)
   1    0.000    0.000    0.000    0.000 sum.py:3(<module>)
   1    0.000    0.000    0.000    0.000 {execfile}
   1    0.000    0.000    0.000    0.000 {method ......}
'''

print ("\n\tabnanny  - The tabnanny Module")
'''
The tabnanny module checks Python source files for ambiguous indentation. 
If a file mixes tabs and spaces in a way that throws off indentation, no 
matter what tab size you're using, the nanny complains −


The tabnanny Module

The tabnanny module checks Python source files for ambiguous indentation. If a file mixes tabs and 
spaces in a way that throws off indentation, no matter what tab size you're using, the nanny complains −
Example

Let us try to profile the following program −

#!/usr/bin/python

vara = 10
varb = 20

sum = vara + varb
print("vara + varb = %d" % sum

If you would try a correct file with tabnanny.py, then it won't complain as follows −

$tabnanny.py -v sum.py
'sum.py': Clean bill of health.

'''







