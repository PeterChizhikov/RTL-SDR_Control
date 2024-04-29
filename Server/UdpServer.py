import time
import socket
from threading import Thread, Lock
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot,QThread
from queue import Empty, Queue
import json
from Structures import SDRData

class UdpServer(QThread, QObject):
    def __init__(self, serverAddr, PortAddr,ClientPort):
        QThread.__init__(self)
        QObject.__init__(self)
        self.fullAddr = (serverAddr, PortAddr)
        self.ClientAddr = (serverAddr, ClientPort)
        

        self.UDPQueue = Queue(maxsize=1e6)


    def saveToQueueSlot(self, cordsToRecive):
        with self.mutex:
            self.UDPQueue.put(cordsToRecive)

    def SDRDataToJson(self,SDRDataCord):
        jsonData = json.dumps(SDRDataCord.__dict__, indent=1)
        return jsonData


    def run(self):
        self.server_udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_udp_socket.bind(self.fullAddr)
        # self.server_udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1024*1024)  # Увеличить до 1MB
        
        self.mutex = Lock()
        print("Udp started on:", self.fullAddr) 
        while True:
            if not self.UDPQueue.empty():
                #объект с точками и т д...
                data = self.UDPQueue.get()
                #data [[],[],[],[],[]]
                pointsArr = []
                for pointIndex in range(len(data.x)):
                    xPoint = data.x[pointIndex]
                    yPoint = data.y[pointIndex]
                    pointsArr.append([xPoint,yPoint])
                # print("value of max point:", data.getMax())
                # print("first element: ", pointsArr[0])
                jsonObj = {
                    "max_frequency" : data.getMax(),
                    "min_frequency" : data.getMin(),
                    "min_magnitude" : data.getMinY(),
                    "max_magnitude": data.getMaxY(),
                    "data": pointsArr
                }
                json_dump_data = json.dumps(jsonObj)
                self.server_udp_socket.sendto(bytearray(json_dump_data, encoding='utf8'), self.ClientAddr)
                
