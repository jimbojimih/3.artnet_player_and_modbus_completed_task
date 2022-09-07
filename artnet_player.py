import socket 
import time
from pymodbus.client.sync import ModbusTcpClient

#modbus
client = ModbusTcpClient('localhost', port = 502)
client.connect()

#artnet
host1 = "localhost" # '192.168.0.1'
host2 = "localhost" #'192.168.0.2' 
port1 = 6454
port2 = 6453
s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s1.connect((host1, port1))
s2.connect((host2, port2))

#open packages
with open('Test_Color.ani', mode='rb') as f: 
    packages = f.read() 

#main loop, delay = 5, number of repetitions = 5
for i in range(5):
    i = 0 #index low
    x = 530 #index hight
    client.write_coil(0x0000, 1, unit = 0x21) 
    client.write_coil(0x0001, 1, unit = 0x21)
    while x <= len(packages):
        package = packages[i:x]
        i += 530
        x += 530            
        byte_14 = package[14]
        if byte_14 == 1:
            s1.sendall(package)                       
        else:
            s2.sendall(package)
        #time.sleep(.025)
        if x > 20000000:
            print(x)
    client.write_coil(0x0000, 0, unit = 0x21) 
    client.write_coil(0x0001, 0, unit = 0x21)
    time.sleep(5)
    
    print('microdone') 
print('done')  
