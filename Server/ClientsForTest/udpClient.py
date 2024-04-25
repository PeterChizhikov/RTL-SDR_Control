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
        plt.cla()
        plt.clf()

        # "max_frequency" : data.getMax(),
        # "min_frequency" : data.getMin(),
        # "min_magnitude" : data.getMinY(),
        # "max_magnitude": data.getMaxY(),
        # "data": pointsArr
                
        #axis([xmin, xmax, ymin, ymax])
        plt.axis([jsonobj["min_frequency"], jsonobj["max_frequency"],
                    jsonobj["min_magnitude"], jsonobj["max_magnitude"]])
        

        for i in range(len(jsonobj["data"])):
            plt.plot(jsonobj["data"][i][0], jsonobj["data"][i][1])
            plt.pause(2)

        plt.show()
        
        



    except socket.timeout: 
        print('REQUEST TIMED OUT')
        
    