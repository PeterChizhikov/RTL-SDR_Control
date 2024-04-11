import socket
from threading import Thread


class TcpServer(Thread):
    def __init__(self, serverAdress, serverPort):
        super().__init__()
        self.serverAdressInfo = (serverAdress, serverPort)
        #AF_INET используется для указания семейства адресов IPv4.
        #SOCK_STREAM используется для указания сокета потока.
        self.daemon = True
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.bind(self.serverAdressInfo)
        self.serverSocket.listen(1)

    def run(self):
        while True:
            print("Tcp started on:", self.serverAdressInfo)    
            # Бесконечно обрабатываем входящие подключения
            client_sock, client_addr = self.serverSocket.accept()
            print('Connected by', client_addr)
            while True:
                # Пока клиент не отключился, читаем передаваемые
                # им данные и отправляем их обратно
                data = client_sock.recv(2048)
                print(data)
                client_sock.sendall(data)
                if not data:
                    # Клиент отключился
                    break
                client_sock.sendall(data)
            client_sock.close()    
        
        
        