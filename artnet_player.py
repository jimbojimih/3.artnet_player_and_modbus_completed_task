import socket 
import time

host1 = "localhost" # '192.168.0.1'
host2 = "localhost" #'192.168.0.2' 
port1 = 6454
port2 = 6453
s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s1.connect((host1, port1))
s2.connect((host2, port2))

with open('Test_Color.ani', mode='rb') as f: 
    packages = f.read() 

for i in range(5):
    i = 0 #index low
    x = 530 #index hight
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
        if x > 15000000:
            print(x)
    time.sleep(5)
    #i = 0 
    #x = 530
    print('microdone') 
print('done')  
