from crypt import methods
from functools import wraps 
import socket 
import threading
from contextlib import closing
from handler import handler 
from datetime import datetime


class Server():
    
    def __init__(self):
        self.routearr = {}

    def run(self, ip, port):
        with closing(socket.socket(socket.AF_INET,socket.SOCK_STREAM)) as server_socket:
            server_name = "ksj_server"
            server_socket.bind((ip, port    ))
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.listen(5)

            # print(self.routearr)

            while True:
                client_socket , addr = server_socket.accept() 

                with closing(client_socket):
                    fd = client_socket.makefile()

                    try:
                        Request_Line = handler(fd)
                        # print(Request_Line)
                        # Request_Line = {'method' : "", 'uri' : "", 'version' : ""}
                    except ValueError:
                        print('invaild msg')
                        fd.close()
                        break
                    if Request_Line['uri'].path == '/':
                        
                        for route in self.routearr.keys():
                            if route == '/':
                                print(self.routearr[route])
                                status_code, header, body = self.routearr[route](Request_Line,fd)
                                
                                response_data = "{0} {1} OK\r\nContent-Type: text/html; charset=ISO-8859-1\r\nServer: {2}\r\nDate: {3}".format(
                                Request_Line['version'], status_code, server_name, datetime.now().strftime('%a, %d %b %Y %H:%M:%S KST'))

                                response_data += "\r\n" + body

                                client_socket.send(response_data.encode('iso-8859-1'))
                        

                    elif Request_Line['method'] == 'POST' and Request_Line['uri'].path == '/post':
                        for route in self.routearr.keys():
                            if route == '/post':
                                print(self.routearr[route])
                                status_code, header, body = self.routearr[route][0](Request_Line,fd)
                                
                                response_data = "{0} {1} OK\r\nContent-Type: text/html; charset=ISO-8859-1\r\nServer: {2}\r\nDate: {3}".format(
                                Request_Line['version'], status_code, server_name, datetime.now().strftime('%a, %d %b %Y %H:%M:%S KST'))

                                response_data += "\r\n" + body

                                client_socket.send(response_data.encode('iso-8859-1'))

                    fd.close()

    def route(path, methods=['GET']):
        def wrap(func):
            self.routearr.append({
                'path': path,
                'methods': methods,
                'handler': func,
            })
            return func
        return wrap 
