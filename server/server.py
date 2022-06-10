from crypt import methods
from functools import wraps 
import socket 
import threading
from contextlib import closing
from handler import handler 

class Server():
    
    def run(self, ip, port):
        with closing(socket.socket(socket.AF_INET,socket.SOCK_STREAM)) as server_socket:

            server_socket.bind((ip, port))
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.listen(5)

            while True:
                client_socket , addr = server_socket.accept() 

                with closing(client_socket):
                    fd = client_socket.makefile()
                    try:
                        Request_Line = handler(fd)
                        print(Request_Line)
                        # Request_Line = {'method' : "", 'uri' : "", 'version' : ""}
                    except ValueError:
                        print('invaild msg')
                    
                    if Request_Line['uri'].path == '/':
                        print('1')
                    
            
    # def __call__(self):
    #     print('call')
    def route(*args, **kwargs):
        def wrapper(func):
            def server():
                print('server') 
        return wrapper