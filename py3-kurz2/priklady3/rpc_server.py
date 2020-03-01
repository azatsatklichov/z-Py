import SimpleXMLRPCServer
def soucet(a,b):
  return a+b
def rozdil(a,b):
  return a-b
server = SimpleXMLRPCServer.SimpleXMLRPCServer(("",8080))
server.register_function(soucet)
server.register_function(rozdil)
server.serve_forever()
