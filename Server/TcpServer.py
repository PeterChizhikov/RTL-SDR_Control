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


    startReadDataFromDeviceSignal = pyqtSignal(json_data)
    stopReadDataFromDeviceSignal = pyqtSignal()
        

    def processComand(self,command):
        print(command)
        if command["type"] == 'system':
            self.startReadDataFromDeviceSignal.emit(command) if command["action"] == 'start' else self.stopReadDataFromDeviceSignal.emit()
        if command["type"] == 'settings': 
            self.getParametersFromJson(command)

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
                    # # self.processComand(json.loads(data.decode('utf8').replace("'", '"')))
                    # x = {
                    #     "answer": 200,
                    # }
                    # y = json.dumps(x)
                    message = SDRConfiguration.SDRConfiguration.from_json(data)
                    client_sock.sendall(bytes(message, encoding='utf8')) 
                if not data:
                    break
            client_sock.close()    
        
        
        