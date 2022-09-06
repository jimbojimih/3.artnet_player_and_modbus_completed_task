import socket 
import time

host1 = '127.0.0.1' # '192.168.0.1'
host2 = '127.0.0.2' #'192.168.0.2' 
port1 = 6454
port2 = 6454
s1 = socket.socket()

s1.connect((host1, port1))


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
        #print(byte_14)
        '''if byte_14 == 1:
            s1.sendall(package)
            data1 = s1.recv(530)
            byte_14_1 = data1[14]
            print(byte_14_1)'''
            
        if byte_14 != 1:
            s1.sendall(package)
            #data2= s2.recv(530)
            #byte_14_2 = data2[14]
            print(s1.recv(530))
        time.sleep(.025)
