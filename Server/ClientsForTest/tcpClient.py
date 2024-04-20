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