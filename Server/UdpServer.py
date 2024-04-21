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

        self.server_udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1024*1024)  # Увеличить до 1MB

        self.ClientAddr = (serverAddr, ClientPort)
        self.mutex = Lock()
        self.read_device_data_status = False
        self.DataFromController = DeviceController.SDRData([0],[0],0,0)
        print("Udp started on:", self.fullAddr) 

        self.UDPQueue = Queue(maxsize=20)


    @Slot(DeviceController.SDRData)
    def saveToQueueSlot(self, cordsToRecive):
        with self.mutex:
            self.UDPQueue.put(self.DataFromController)

    def SDRDataToJson(self,SDRData):
        jsonData = json.dumps(SDRData.__dict__, indent=1)
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
            if not self.UDPQueue.empty():
                # if not self.UDPQueue.empty():   
                data = self.UDPQueue.get()
                json = self.SDRDataToJson(data)
                #TODO JSON
                self.server_udp_socket.sendto(bytes(str("ok"), encoding='utf8'), self.ClientAddr)
            #сохдать очередь и доставаать
            else:
                self.server_udp_socket.sendto(bytes(str("err"), encoding='utf8'), self.ClientAddr)



    # def __del__(self):
    #    if self.server_udp_socket:
    #        self.server_udp_socket.close()
    #        self.cordsQueue.join()



    #python struct iterpack 