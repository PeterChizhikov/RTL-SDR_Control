import time
import socket
from threading import Thread, Lock
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from queue import Empty, Queue
import json
from Structures import SDRData

class UdpServer(Thread, QObject):
    def __init__(self, serverAddr, PortAddr,ClientPort):
        Thread.__init__(self)
        QObject.__init__(self)
        self.fullAddr = (serverAddr, PortAddr)
        self.server_udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_udp_socket.bind(self.fullAddr)

        # self.server_udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1024*1024)  # Увеличить до 1MB

        self.ClientAddr = (serverAddr, ClientPort)
        self.mutex = Lock()
        print("Udp started on:", self.fullAddr) 

        self.UDPQueue = Queue(maxsize=1e6)


    def saveToQueueSlot(self, cordsToRecive):
        print("cords ", len(cordsToRecive))
        with self.mutex:
            self.UDPQueue.put(cordsToRecive.decode())

    def SDRDataToJson(self,SDRData):
        jsonData = json.dumps(SDRData.__dict__, indent=1)
        return jsonData


    def run(self):
        i = 0
        while True:
           
            if not self.UDPQueue.empty():
                # if not self.UDPQueue.empty():   
                data = self.UDPQueue.get()
                json = self.SDRDataToJson(data)
                #TODO JSON
                print("udp sent")
                # self.server_udp_socket.sendto(bytes(str("ok"), encoding='utf8'), self.ClientAddr)
            #сохдать очередь и доставаать
            else:
                self.server_udp_socket.sendto(bytes(str("err"), encoding='utf8'), self.ClientAddr)
