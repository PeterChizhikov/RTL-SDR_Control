import socket
from threading import Thread
import json
from PyQt5.QtCore import QObject, pyqtSignal
import requests

class TcpServer(Thread, QObject):
    def __init__(self, serverAdress, serverPort):
        Thread.__init__(self)
        QObject.__init__(self)
        self.serverAdressInfo = (serverAdress, serverPort)
        self.daemon = True
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.bind(self.serverAdressInfo)
        self.serverSocket.listen(1)

    startReadDataFromDeviceSignal = pyqtSignal()
    stopReadDataFromDeviceSignal = pyqtSignal()
        

    def processComand(self,command):
        print(command)
        if command["type"] == 'system':
            self.startReadDataFromDeviceSignal.emit() if command["action"] == 'start' else self.stopReadDataFromDeviceSignal.emit()
        if command["type"] == 'settings': 
            self.getParametersFromJson(command)

    def getParametersFromJson(self, jsonData):
        print('')

    def run(self):
        while True:
            print("Tcp started on:", self.serverAdressInfo)    
            client_sock, client_addr = self.serverSocket.accept()
            print('Connected by', client_addr)
            while True:
                data = client_sock.recv(2048)  
                #qt: 
                self.processComand(json.loads(data.decode('utf8')))
                # self.processComand(json.loads(data.decode('utf8').replace("'", '"')))
                x = {
                    "answer": 200,
                }
                y = json.dumps(x)
                client_sock.sendall(bytes(y, encoding='utf8')) 
                if not data:
                    break
            client_sock.close()    
        
        
        