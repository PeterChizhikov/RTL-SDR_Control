import socket
import time
import json


client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_sock.connect(('127.0.0.1', 5577))


x = {
  "type": "system",
  "action": "start"
}

# convert into JSON:
y = json.dumps(x)

# the result is a JSON string:
# print(y)


# string = 'Hello, world ' + str(i)
client_sock.sendall(bytes(y, encoding='utf8')) 

time.sleep(20)

x2 = {
  "type": "system",
  "action": "stop"
}

# convert into JSON:
y2 = json.dumps(x2)

# the result is a JSON string:
# print(y)


# string = 'Hello, world ' + str(i)
client_sock.sendall(bytes(y2, encoding='utf8')) 


# data = client_sock.recv(1024)
# print('Received', repr(data))
# # i = i + 1
# time.sleep(0.4)
   

# client_sock.close()
# print('Received', repr(data))

