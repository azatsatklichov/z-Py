#!/usr/bin/python

import sys, getopt


def main(argv):
   inputfile = ''
   outputfile = ''
   try:
      opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
   except getopt.GetoptError:
      print("'ERR, right usage: test.py -i <inputfile> -o <outputfile>')")
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print("'test.py -i <inputfile> -o <outputfile>')")
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
   print("Input file is ", inputfile)
   print("Output file is ", outputfile)

if __name__ == "__main__":
    last_list = [1,2,3]
    if last_list[1:]:
        print(last_list[1:])
    empty_list = []
    print("empty_list[:1])")
    main(sys.argv[1:])
   

#Now, run above script as follows
# test.py -h
#usage: test.py -i <inputfile> -o <outputfile>
# test.py -i BMP -o
#usage: test.py -i <inputfile> -o <outputfile>
# test.py -i inputfile
#Input file is " inputfile
#Output file is "

