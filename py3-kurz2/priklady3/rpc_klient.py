import xmlrpclib
server = xmlrpclib.ServerProxy("http://10.2.21.199:8080/")
v = server.soucet(2,3)
print(v)
