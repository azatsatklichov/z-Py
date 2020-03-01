import sqlite3
conn = sqlite3.connect("phones.sqlite")
cursor = conn.cursor()
cursor.execute("select * from phones")
for record in cursor.fetchall():
    print(record)
  # print("Name : %s, phone number : %s" % (record[0], record[1]))
conn.close()
