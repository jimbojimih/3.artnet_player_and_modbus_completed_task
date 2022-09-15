import socket
from threading import Thread

def run(host, port):
    '''open server'''
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        conn, addr = s.accept()
        with conn:
            while True:
                data = conn.recv(4096)
                print(data[14])

for host in ['127.0.0.1', '127.0.0.2']:
    for port in [6454]:
        thread = Thread(target=run, args=(host, 6454))
        thread.start()
