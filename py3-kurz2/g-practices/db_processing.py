'''
Python defines Python Database API Specification v2.0
Relational databases are the most widely used type of database,
storing information as tables containing a number of rows.
'''

#Example SQlite
import sqlite3

conn=sqlite3.connect("phones.sqlite")
cursor=conn.cursor()
cursor.execute("select * from phones")

for record in cursor.fetchall():
	print("Name : %s, phone number : %s" %(record[0],record[1]))
conn.close()
