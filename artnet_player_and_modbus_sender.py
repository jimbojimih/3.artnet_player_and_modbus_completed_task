import socket 
import time
from threading import Thread
from pymodbus.client.sync import ModbusTcpClient

class ModbusBroadcast():    
    
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.outputs = []
        self.units = []    
        
    def connect(self):
        self.client = ModbusTcpClient(self.host, self.port)
        self.client.connect()
        
    def set_broadcast_settings(self, outputs, modules):
        self.outputs = outputs
        self.modules = modules
        
    def write_coil_false(self):
        for module in self.modules:
            for output in self.outputs:
                self.client.write_coil(output, 0, unit=module)
                self.client.write_coil(output, 0, unit=module)
        
    def write_coil_true(self):
        for module in self.modules:
            for output in self.outputs:
                self.client.write_coil(output, 1, unit=module)
                self.client.write_coil(output, 1, unit=module)

                
class ArtnetBroadcast():
    def __init__(self, host, port):
        self.host = host
        self.port = port    
        
    def connect(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.host, self.port))

    def send(self, package):
        self.package = package
        self.s.sendall(self.package)
        
        
class Packages():
    def __init__(self, packages_file):
        self.packages_file = packages_file
        self.packages = b''
        
    def open(self):
        with open(self.packages_file, mode='rb') as f: 
            self.packages = f.read()
            
    def get_file(self):
        return self.packages
    

if __name__ == '__main__':
    
    modbus_broadcast = ModbusBroadcast('localhost', 502)
    modbus_broadcast.connect()
    outputs = [0x0000, 0x0001]
    modules = [0x21]
    modbus_broadcast.set_broadcast_settings(outputs, modules)
    
    packages = Packages('Test_Color.ani')
    packages.open()
    bytes_string = packages.get_file()
    
    art1 = ArtnetBroadcast("127.0.0.1", 6454)
    art_other = ArtnetBroadcast("127.0.0.2", 6454)
    art1.connect()
    art_other.connect()
    for i in range(5):
            index_low = 0 
            index_hight = 530 
            modbus_broadcast.write_coil_true() 
            while index_hight <= len(bytes_string):
                package = bytes_string[index_low:index_hight]
                index_low += 530
                index_hight += 530            
                byte_14 = package[14]
                if byte_14 == 1:
                    art1.send(package)                       
                else:
                    art_other.send(package)
                #time.sleep(.025)
                if index_hight > 20000000:
                    print(index_hight)
            modbus_broadcast.write_coil_false() 
            time.sleep(5)


