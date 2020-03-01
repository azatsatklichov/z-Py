import cx_Oracle
conn=cx_Oracle.connect("hr/hr@10.2.20.118:1521/orcl")
cursor=conn.cursor()
cursor1=conn.cursor()
radky=[('prvni','1'),('druhy','2'),('treti','3')]
#cursor1.execute("insert into phones values ('Policie','158')")
#conn.commit()
cursor1.executemany("insert into phones values (:a,:b)",radky)
conn.commit()
cursor.execute("select * from phones")
for record in cursor.fetchall():
  print("Name : %s, phone number : %s" %(record[0],record[1]))
conn.close()
