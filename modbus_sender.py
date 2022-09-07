from pymodbus.client.sync import ModbusTcpClient

client = ModbusTcpClient('localhost', port = 502)
client.connect()
# 0 - false, 1 - true
client.write_coil(0x00, 0, unit = 0x21) 
client.write_coil(0x01, 0, unit = 0x21)


