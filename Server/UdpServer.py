import time
import socket
from threading import Thread


class UdpServer(Thread):
    def __init__(self, serverAddr, PortAddr,ClientPort):
        super().__init__()
        self.fullAddr = (serverAddr, PortAddr)
        self.server_udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_udp_socket.bind(self.fullAddr)
        self.ClientAddr = (serverAddr, ClientPort)
        print("Udp started on:", self.fullAddr) 
    def run(self):
        i = 0
        while True:
            message="Num from udp: " + str(i)
            i = i +1
            time.sleep(0.6)
            self.server_udp_socket.sendto(bytes(message, encoding='utf8'), self.ClientAddr)


