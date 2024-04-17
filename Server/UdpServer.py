import time
import socket
from threading import Thread, Lock
from PySide6.QtCore import QObject, Signal, Slot
from queue import Empty, Queue
import json
from DeviceController import SDRData

class UdpServer(Thread, QObject):
    def __init__(self, serverAddr, PortAddr,ClientPort):
        Thread.__init__(self)
        QObject.__init__(self)
        self.fullAddr = (serverAddr, PortAddr)
        self.server_udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_udp_socket.bind(self.fullAddr)
        self.ClientAddr = (serverAddr, ClientPort)
        self.mutex = Lock()
        self.read_device_data_status = False
        self.cordsQueue = Queue()
        print("Udp started on:", self.fullAddr) 


    @Slot()
    def saveToQueueSlot(self, cordsToRecive):
        with self.mutex:
            self.read_device_data_status = False
        self.cordsQueue = cordsToRecive

    def arrayToJson(array):
        dictionary = {x:array[0],y:array[1],minf:array[2],maxf:array[3]}
        return json.dumps(dictionary)

        # class SDRData():
        #     def __init__(self,x,y,minf,maxf):
        #         self.cords = [x,y]
        #         self.minf = minf 
        #         self.maxf = maxf


    def run(self):
        i = 0
        while True:
            message ="Num from udp: " + str(i)
            # message = ""
            i = i +1
            time.sleep(0.6)
            if len(message) != 0:
                self.server_udp_socket.sendto(bytes(message, encoding='utf8'), self.ClientAddr)
            with self.mutex:
                self.read_device_data_status = True
                while not self.cordsQueue.empty():
                    print("cordrs on udp", cordsQueue)
                    data = self.cordsQueue.get()
                    json = arrayToJson(data)
                    #self.server_udp_socket.sendto(bytes(json, encoding='utf8'), self.ClientAddr)