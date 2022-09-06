import socket
HOST = '127.0.0.1'  
PORT = 6453        
with socket.socket() as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(530)
            if not data:
                break
            
            conn.sendall(data)
