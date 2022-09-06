import socket 
import time
from threading import Thread

host1 = '127.0.0.1' # '192.168.0.1'
host2 = '127.0.0.2' #'192.168.0.2' 
port = 6454
s1 = socket.socket()
s2 = socket.socket()
s1.connect((host1, port))
s2.connect((host2, port))

with open('Test_Color.ani', mode='rb') as f: 
    packages = f.read()
i = 0
x = 530
while True:
    for package in packages:    
        package = packages[i:x]
        i += 530
        x += 530            
        byte_14 = package[14]
        if byte_14 == 1:
            s1.sendall(package)                       
        else:
            s2.sendall(package)
        time.sleep(.025)
