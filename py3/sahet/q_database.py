'''
Created on Jan 7, 2018

@author: satklichov
'''

'''
try:
    conn = psycopg2.connect("dbname='sx' user='dbuser' host='localhost' password='postgres'")
except:
    print ("I am unable to connect to the database")
'''

#https://wiki.postgresql.org/wiki/Python
import psycopg2


def main():
    # Define our connection string
    conn_string = "host='localhost' dbname='pyuser' user='pyuser' password='pyuser'"
 
    # print the connection string we will use to connect
    print ("Connecting to database\n    ->%s" % (conn_string))
 
    # get a connection, if a connect cannot be made an exception will be raised here
    conn = psycopg2.connect(conn_string)
 
    # conn.cursor will return a cursor object, you can use this cursor to perform queries
    cursor = conn.cursor()
    print ("Connected!\n")
    
    
    # execute SQL query using execute() method.
    cursor.execute("SELECT VERSION()")

    # Fetch a single row using fetchone() method.
    data = cursor.fetchone()
    print ("Database version : %s " % data)

    # disconnect from server
    conn.close()

 
if __name__ == "__main__":
    main() 
