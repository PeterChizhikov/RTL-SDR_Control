import socket
import time

UDP_IP = "127.0.0.1"
UDP_PORT = 6643

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

sock.bind((UDP_IP, UDP_PORT))


while True:
    print("a")
    time.sleep(0.1)
    message = "JJ"
    try:
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        print("received message: %s" % data)
    except socket.timeout: 
        print('REQUEST TIMED OUT')
        
    