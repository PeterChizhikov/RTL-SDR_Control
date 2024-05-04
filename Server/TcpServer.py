import socket
from threading import Thread
import json
from PyQt5.QtCore import QObject, pyqtSignal,QThread
import requests
from Structures import SDRConfiguration

class TcpServer(QThread, QObject):
    def __init__(self, serverAdress, serverPort):
        QThread.__init__(self)
        QObject.__init__(self)
        self.servAdr = serverAdress
        self.port = serverPort


    startReadDataFromDeviceSignal = pyqtSignal(str)
    stopReadDataFromDeviceSignal = pyqtSignal()
        

    def processComand(self,command,json):
        print(command)
        if command["type"] == 'system':
            self.startReadDataFromDeviceSignal.emit(json) if command["action"] == 'start' else self.stopReadDataFromDeviceSignal.emit()
        if command["type"] == 'settings': 
            self.getParametersFromJson()

    def getParametersFromJson(self, jsonData):
        print('')

    def run(self):
        self.serverAdressInfo = (self.servAdr, self.port)
        self.daemon = True
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.bind(self.serverAdressInfo)
        self.serverSocket.listen(1)
        while True:
            print("Tcp started on:", self.serverAdressInfo)    
            client_sock, client_addr = self.serverSocket.accept()
            print('Connected by', client_addr)
            while True:
                data = client_sock.recv(2048)  
                #qt:
                if len(data) != 0: 
                    # self.processComand(json.loads(data.decode('utf8')))
                    self.processComand(json.loads(data.decode('utf8').replace("'", '"'))
                        ,data.decode('utf8').replace("'", '"'))
                    x = {
                        "type": "settings",
                        "sample_rate": "2.048e6",
                        "center_frequency": "60e6",
                        "frequency_correction": "60" ,
                        "gain": "auto",
                    }
                    y = json.dumps(x)
                    message = SDRConfiguration.SDRConfiguration.from_json(y)
                    client_sock.sendall(bytes(message, encoding='utf8')) 
                if not data:
                    break
            client_sock.close()    
        
        
        