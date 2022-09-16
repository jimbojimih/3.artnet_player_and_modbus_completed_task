import socket 
import time

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
    

class Sender():
    
    def __init__(self, bytes_string, modbus_broadcast, *artnet_list):
        self.bytes_string = bytes_string
        self.modbus_broadcast = modbus_broadcast
        self.artnet_list = artnet_list  
        
    def send_type_1(self, sleep_for_freq, delay, repeat):
        
        ''' Sending packages to 2 artnet converters. Pacages with

        universe address 1 go to art_net_1, all othe packages go
        
        to art_net_other. At the start and end packages
        
        transmission, relay modules are controlled.
        
        '''
        
        self.sleep_for_freq = sleep_for_freq
        self.delay = delay
        self.repeat = repeat
        
        art_net_1 = self.artnet_list[0]
        art_net_other = self.artnet_list[1]
        
        for i in range(self.repeat):
            index_low = 0 
            index_hight = 530 
            self.modbus_broadcast.write_coil_true() 
            while index_hight <= len(bytes_string):
                package = self.bytes_string[index_low:index_hight]
                index_low += 530
                index_hight += 530            
                byte_14 = package[14]
                if byte_14 == 1:
                    art_net_1.send(package)                       
                else:
                    art_net_other.send(package)
                time.sleep(sleep_for_freq)
            self.modbus_broadcast.write_coil_false() 
            time.sleep(self.delay)

    
if __name__ == '__main__':        
    
    modbus_broadcast = ModbusBroadcast('192.168.0.10', 8234)
    modbus_broadcast.connect()
    outputs = [0x0000, 0x0001]
    modules = [0x21]
    modbus_broadcast.set_broadcast_settings(outputs, modules)
    
    packages = Packages('Test_Color.ani')
    packages.open()
    bytes_string = packages.get_file()
    
    art_1 = ArtnetBroadcast("192.168.0.1", 6454)
    art_other = ArtnetBroadcast("192.168.0.2", 6454)
    art_net_list = [art_1, art_other]
    for art_net in art_net_list:
        art_net.connect()
        
    sender = Sender(bytes_string, modbus_broadcast, *art_net_list)
    sender.send_type_1(0.25, 5, 5)

