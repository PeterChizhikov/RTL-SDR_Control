import socket
from threading import Condition
from threading import Lock
import json
from PyQt5.QtCore import QObject, pyqtSignal,QThread
from PyQt5.QtCore import QObject, pyqtSignal,QThread
from Structures import SDRConfiguration

class TcpServer(QThread, QObject):
    def __init__(self, serverAdress, serverPort):
        QThread.__init__(self)
        QObject.__init__(self)
        self.servAdr = serverAdress
        self.port = serverPort
        self.commandAccepted = 409
        self.mut = Lock()
        self.cv = Condition()

    startReadDataFromDeviceSignal = pyqtSignal()
    stopReadDataFromDeviceSignal = pyqtSignal()
    setNewSettingsSignal = pyqtSignal(list)

    def processComand(self,command):
        if command["type"] == 'system':
            self.startReadDataFromDeviceSignal.emit() if command["action"] == 'start' else self.stopReadDataFromDeviceSignal.emit()
        if command["type"] == 'settings': 
            self.getParametersFromJson(command)

    def getParametersFromJson(self, jsonData):
        message = [float(jsonData["sample_rate"]), 
                   int(jsonData["center_frequency"]),
                   int(jsonData["frequency_correction"]),]
        
        message.append("auto") if str(jsonData["gain"]) == "auto" else message.append(float(jsonData["gain"]))
    
        

        if len(message) != 0:
            self.setNewSettingsSignal.emit(message)
        else:
            with self.cv:
                self.commandAccepted = 409
                self.cv.notify_all()
            
    def startAndStopReadDataFromDeviceResponseSlot(self, status):
        with self.cv:
            self.commandAccepted = status
            self.cv.notify_all()

    def setSettingsResponseSlot(self, status):
        with self.cv:
            self.commandAccepted = status
            self.cv.notify_all()

    def formResponseMessage(self, status):
        x = {
            "answer": status,
        }
        return x

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
                if len(data) != 0: 
                    with self.cv:
                        self.processComand(json.loads(data.decode('utf8')))
                        self.cv.wait()
                        y = json.dumps(self.formResponseMessage(self.commandAccepted))
                        print(y)
                        client_sock.sendall(bytes(y, encoding='utf8')) 
                if not data:
                    break
            client_sock.close()