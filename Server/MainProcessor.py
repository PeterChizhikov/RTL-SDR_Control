from TcpServer import TcpServer 
from UdpServer import UdpServer
from DeviceController import DeviceController 

from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal, Qt

from queue import Empty, Queue


TCP_PORT = 5577
UDP_SERVER_PORT = 6644
UDP_CLIENT_PORT = 6643
SERVER_ADRESS = 'localhost'



class MainProcessor:
    def __init__(self):


        self.deviceController = DeviceController(2.048e6, 60e6, 60, 'auto', 256*1024)
        self.tcpServer = TcpServer(SERVER_ADRESS,TCP_PORT)
        self.udpServer = UdpServer(SERVER_ADRESS,UDP_SERVER_PORT, UDP_CLIENT_PORT)


        self.tcpServer.startReadDataFromDeviceSignal.connect(self.deviceController.startReadDeviceDataSlot, Qt.DirectConnection)
        self.tcpServer.stopReadDataFromDeviceSignal.connect(self.deviceController.stopReadDeviceDataSlot,Qt.DirectConnection)
        self.deviceController.saveToQueueSignal.connect(self.udpServer.saveToQueueSlot,Qt.DirectConnection)

        
        self.tcpServer.start()
        self.udpServer.start()
        self.deviceController.start()


