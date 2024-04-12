from TcpServer import TcpServer 
from UdpServer import UdpServer
from DeviceController import DeviceController 
import time

TCP_PORT = 5577
UDP_SERVER_PORT = 6644
UDP_CLIENT_PORT = 6643
SERVER_ADRESS = 'localhost'

class MainProcessor:
    def __init__(self):
        self.tcpServer = TcpServer(SERVER_ADRESS,TCP_PORT)
        self.tcpServer.start()
        self.udpServer = UdpServer(SERVER_ADRESS,UDP_SERVER_PORT, UDP_CLIENT_PORT)
        self.udpServer.start()


        self.deviceController = DeviceController(2.048e6,
                                                70e6,60,
                                                'auto',
                                                512)
        samples = self.deviceController.readDeviceData()
        print(samples)
        
