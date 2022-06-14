# import socket
# from contextlib import closing 
# HOST = 'localhost'
# PORT = 8080

# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# with closing(client_socket) as c:
#     c.connect((HOST, PORT))
#     # data = input()
#     c.send(b'Hello')

import requests

URL = 'localhost:8081'

