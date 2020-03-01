import cx_Oracle
conn = cx_Oracle.connect("hr/hr@10.2.20.118:1521/orcl")
cursor = conn.cursor()
cursor.execute("select * from phones")
for record in cursor.fetchall():
  print("Name : %s, phone number : %s" % (record[0], record[1]))
conn.close()
