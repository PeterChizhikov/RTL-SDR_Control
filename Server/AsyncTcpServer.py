import socket
from threading import Condition
from threading import Lock
import json
from PyQt5.QtCore import QObject, pyqtSignal,QThread
from PyQt5.QtCore import QObject, pyqtSignal,QThread

import asyncio




class AsyncTcpServer(QObject):
    def __init__(self, serverAdress, serverPort):
        QObject.__init__(self)
        self.servAdr = serverAdress
        self.port = serverPort

        self.loop = asyncio.new_event_loop()
        self.loop.run_until_complete(self.run_server())

        self.commandAccepted = 409
        self.mut = Lock()
        self.cv = Condition()


    startReadDataFromDeviceSignal = pyqtSignal()
    stopReadDataFromDeviceSignal = pyqtSignal()
    setNewSettingsSignal = pyqtSignal(list)

    async def handle_echo(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        data = None

        while data != b"quit":
            data = await reader.read(1024)
            msg = data.decode()
            addr, port = writer.get_extra_info("peername")
            print(f"Message from {addr}:{port}: {msg!r}")




            writer.write(data)
            await writer.drain()

        writer.close()
        await writer.wait_closed()



    async def run_server(self) -> None:
        server = await asyncio.start_server(self.handle_echo, self.servAdr, self.port)
        async with server:
            await server.serve_forever()




    # def processComand(self,command):
    #     print("1**********************")
    #     if command["type"] == 'system':
    #         self.startReadDataFromDeviceSignal.emit() if command["action"] == 'start' else self.stopReadDataFromDeviceSignal.emit()
    #     if command["type"] == 'settings': 
    #         self.getParametersFromJson(command)

    # def getParametersFromJson(self, jsonData):
    #     self.commandAccepted = 409
    #     message = [float(jsonData["sample_rate"]), 
    #                float(jsonData["center_frequency"]),
    #                float(jsonData["frequency_correction"]),
    #                float(jsonData["gain"]),]
    #     if len(message) != 0:
    #         self.setNewSettingsSignal.emit(message)
    #     else:
    #         with self.cv:
    #             self.commandAccepted = 409
    #             self.cv.notify_all()
            
    # def startAndStopReadDataFromDeviceSlot(self, status):
    #     print("4**********************")
    #     with self.cv:
    #         self.commandAccepted = status
    #         print("startAndStopReadDataFromDeviceSlot", status)
    #         self.cv.notify_all()

    # def setSettingsResponseSlot(self, status):
    #     with self.cv:
    #         self.commandAccepted = status
    #         self.cv.notify_all()

    # def formResponseMessage(self, status):
    #     print("status")
    #     x = {
    #         "answer": status,
    #     }
    #     return x

    # def run(self):
    #     self.serverAdressInfo = (self.servAdr, self.port)
    #     self.daemon = True
    #     self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     self.serverSocket.bind(self.serverAdressInfo)
    #     self.serverSocket.listen(1)
    #     while True:
    #         print("Tcp started on:", self.serverAdressInfo)    
    #         client_sock, client_addr = self.serverSocket.accept()
    #         print('Connected by', client_addr)
    #         while True:
    #             data = client_sock.recv(2048)  
    #             print("Data received", data)
    #             if len(data) != 0: 
    #                 with self.cv:
    #                     self.processComand(json.loads(data.decode('utf8')))

    #                     self.cv.wait()
    #                     print("5**********************")
    #                     y = json.dumps(self.formResponseMessage(self.commandAccepted))
    #                     print(y)
    #                     client_sock.sendall(bytes(y, encoding='utf8')) 
    #                     data = ""
    #             if not data:
    #                 break
    #         client_sock.close()