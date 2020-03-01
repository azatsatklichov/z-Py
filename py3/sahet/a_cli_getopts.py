'''
Created on Jun 2, 2018

@author: ASUS
'''
#!/usr/bin/python
import sys, getopt

print('\nThis method parses command line options and parameter list. Following is simple syntax for this method \n')

'''
HOW to RUN
$ a_cli_getopts.py -i BMP -o
usage: test.py -i <inputfile> -o <outputfile>

$ a_cli_getopts.py -i inputfile
Input file is " inputfile
Output file is "

python a_cli_getopts.py  -i BMP

Input file is " BMP
Output file is "
'''
def main(argv):
   inputfile = ''
   outputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print('test.py -i <inputfile> -o <outputfile>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print( 'test.py -i <inputfile> -o <outputfile>')
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
   print('Input file is "', inputfile)
   print('Output file is "', outputfile)


if __name__ == "__main__":
   main(sys.argv[1:])
