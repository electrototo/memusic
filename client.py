import time
import socket
import json

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(1.0)
message = b'test'
addr = ("127.0.0.1", 12000)

str_data = {
    'color': 'rojo',
    'x': -3,
    'y': 1
}

message = bytes(json.dumps(str_data), 'utf-8')
client_socket.sendto(message, addr)
