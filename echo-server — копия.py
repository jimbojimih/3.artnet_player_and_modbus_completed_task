import socket
HOST = '127.0.0.2'  
PORT = 6454        
with socket.socket() as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        print(s)
        while True:
            data = conn.recv(530)
            print(data[14])
            if not data:
                break
            
            conn.sendall(data)
