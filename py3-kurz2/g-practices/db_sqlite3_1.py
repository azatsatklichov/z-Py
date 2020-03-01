'''
Python defines Python Database API Specification v2.0
Relational databases are the most widely used type of database,
storing information as tables containing a number of rows.
'''
#!/usr/bin/python

import sqlite3

conn = sqlite3.connect('test.db')
print("Opened database successfully")


#http://zetcode.com/db/sqlitepythontutorial/
