
'''
Python provides two levels of access to network services. At a low level, you can access the basic socket support in 
the underlying operating system, which allows you to implement clients and servers for both connection-oriented and connectionless protocols.

Python also has libraries that provide higher-level access to specific application-level network protocols, 
such as FTP, HTTP, and so on.

'''

import socket  # Import socket module

s = socket.socket()  # Create a socket object
host = socket.gethostname()  # Get local machine name

print(host)

port = 12345  # Reserve a port for your service.
s.bind((host, port))  # Bind to the port

s.listen(5)  # Now wait for client connection.
while True:
   c, addr = s.accept()  # Establish connection with client.
   print ('Got connection from', addr)
   c.send('Thank you for connecting')
   c.close()  # Close the connection
