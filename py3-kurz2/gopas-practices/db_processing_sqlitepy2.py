'''
Python defines Python Database API Specification v2.0
Relational databases are the most widely used type of database,
storing information as tables containing a number of rows.
'''

#Example SQlite
import sqlite3

#https://docs.python.org/2/library/sqlite3.html

conn=sqlite3.connect("phones.sqlite")
cursor1=conn.cursor()
cursor2=conn.cursor()

cursor1.execute("insert into phones values('Police', '911')")
conn.commit()
cursor2.execute("select * from phones")

for record in cursor2.fetchall():
	print("Name : %s, phone number : %s" %(record[0],record[1]))
conn.close()

