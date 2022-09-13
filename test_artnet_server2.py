import socket
HOST = '10.1.3.28'  
PORT = 6454        
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        #print('Connected by', addr)
        
        while True:
            data = conn.recv(4096)
