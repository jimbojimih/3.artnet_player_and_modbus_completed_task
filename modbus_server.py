import modbus_server as se
s = se.Server(port=5020)
s.start()
s.set_coil(1,True)
