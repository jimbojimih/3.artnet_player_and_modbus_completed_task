import socket
HOST = '127.0.0.2'  
PORT = 6454        
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:        
        while True:
            data = conn.recv(4096)
