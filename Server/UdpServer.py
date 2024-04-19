import time
import socket
from threading import Thread, Lock
from PySide6.QtCore import QObject, Signal, Slot
from queue import Empty, Queue
import json
from DeviceController import DeviceController

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


    @Slot(DeviceController.SDRData)
    def saveToQueueSlot(self, cordsToRecive):
        with self.mutex:
            self.read_device_data_status = False
            self.cordsQueue = cordsToRecive

    def SDRDataToJson(SDRData):
        jsonData = json.dumps(SDRData.to_dict(), indent=4)
        return jsonData

        # class SDRData:
        #     def __init__(self,x,y,minf,maxf):
        #         self.cords = [x,y]
        #         self.minf = minf 
        #         self.maxf = maxf


    def run(self):
        i = 0
        while True:
            # self.server_udp_socket.sendto(bytes(str(123), encoding='utf8'), self.ClientAddr)
            if not self.cordsQueue.empty():
                data = self.cordsQueue.get()
                json = SDRDataToJson(data)
                self.server_udp_socket.sendto(bytes(str(json), encoding='utf8'), self.ClientAddr)


    # def __del__(self):
    #    if self.server_udp_socket:
    #        self.server_udp_socket.close()
    #        self.cordsQueue.join()