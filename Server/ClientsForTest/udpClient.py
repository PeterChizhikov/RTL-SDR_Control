import socket
import time
import json
import numpy as np
import matplotlib.pyplot as plt

UDP_IP = "127.0.0.1"
UDP_PORT = 6643

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

sock.bind((UDP_IP, UDP_PORT))

i = 0
while True:
    try:
        data, addr = sock.recvfrom(1024*1024) # buffer size is 1024 bytes
        byte = data.decode("utf-8").replace("'", '"')
        jsonobj = json.loads(byte)
        print(jsonobj)
        
        



    except socket.timeout: 
        print('REQUEST TIMED OUT')
        
    