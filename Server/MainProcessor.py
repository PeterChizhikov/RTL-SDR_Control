from TcpServer import TcpServer 
from UdpServer import UdpServer
from DeviceController import DeviceController 
from AsyncTcpServer import AsyncTcpServer

from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal, Qt,QEventLoop,QThread
from PyQt5.QtWidgets import QApplication
from queue import Empty, Queue
import sys
import time

TCP_PORT = 5577
UDP_SERVER_PORT = 6644
UDP_CLIENT_PORT = 6643
SERVER_ADRESS = 'localhost'


class MainProcessor():
    def __init__(self):
        self.deviceControllerThread = QThread()
        self.udpThread = QThread()
        self.tcpThread = QThread()

        self.deviceController = DeviceController(2.048e6, 60e6, 60, 'auto', 1024)
        self.tcpServer = TcpServer(SERVER_ADRESS,TCP_PORT)
        self.udpServer = UdpServer(SERVER_ADRESS,UDP_SERVER_PORT, UDP_CLIENT_PORT)
        

        self.tcpServer.start()
        self.udpServer.start()
        self.deviceController.start()

        self.tcpServer.startReadDataFromDeviceSignal.connect(self.deviceController.startReadDeviceDataSlot, Qt.DirectConnection)
        self.tcpServer.stopReadDataFromDeviceSignal.connect(self.deviceController.stopReadDeviceDataSlot,Qt.DirectConnection)
        self.deviceController.saveToQueueSignal.connect(self.udpServer.saveToQueueSlot,Qt.DirectConnection)  
        self.tcpServer.setNewSettingsSignal.connect(self.deviceController.setNewSettingsSlot, Qt.DirectConnection)
        self.deviceController.setSettingsResponseSignal.connect(self.tcpServer.setSettingsResponseSlot,Qt.DirectConnection)
        self.deviceController.startAndStopReadDataFromDeviceResponseSignal.connect(self.tcpServer.startAndStopReadDataFromDeviceResponseSlot, Qt.DirectConnection)


        loop = QEventLoop()
        sys.exit(loop.exec_())

