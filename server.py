import random
import socket
import json

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('', 12000))

while True:
    rand = random.randint(0, 10)
    message, address = server_socket.recvfrom(1024)

    message = message.decode('utf-8')
    data = json.loads(message)

    print('color: {}'.format(data['color']))
    print('x: {}, y: {}'.format(data['x'], data['y']))
