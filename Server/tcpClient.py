import socket
import time
client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_sock.connect(('127.0.0.1', 5577))

i = 0
while i < 100:
    string = 'Hello, world ' + str(i)
    client_sock.sendall(bytes(string, encoding='utf8')) 
    data = client_sock.recv(1024)
    print('Received', repr(data))
    i = i + 1
    time.sleep(0.4)
   

client_sock.close()
print('Received', repr(data))

