from crypt import methods
from functools import wraps 
import socket 
import threading
from contextlib import closing
from time import sleep
from handler import handler, ParserState
from datetime import datetime
from pprint import pprint

class Server():
    
    def __init__(self):
        self.routearr = []
        self.www_auth = []

    def run(self, ip, port):
        with closing(socket.socket(socket.AF_INET,socket.SOCK_STREAM)) as server_socket:
           
            server_socket.bind((ip, port))
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.listen(5)


            while True:
                client_socket , addr = server_socket.accept() 
                t1 = threading.Thread(target=self.cli, args = (client_socket,))
                t1.start()

                # thread stop


                


    def cli(self, client_socket):
        with closing(client_socket):
            fd = client_socket.makefile()

            try:
                Request_Line, headers = handler(fd)
                # Request_Line = {'method' : "", 'path' : "", 'version' : ""}
            except ValueError:
                print('invaild http msg')
                fd.close()

            # HTTP response
            for routear in self.routearr:                
                if routear['path'] == Request_Line['path'].path and\
                    Request_Line['method'] in routear['methods']:
                    status_code, header, body = routear['handler'](headers,fd)
                    
                    ### response data 
                    server_name = "ksj_server"
                    response_data = \
                        "{0} {1} OK\r\nContent-Type: text/html; charset=ISO-8859-1\r\nServer: {2}\r\nDate: {3}".format(\
                    Request_Line['version'], status_code\
                    , server_name,\
                    datetime.now().strftime('%a, %d %b %Y %H:%M:%S KST'))
                    
                    response_data += '\r\n' + body
                        
                    # why is stop 
                    # HTTP request header 
                    # sleep(5)


                    client_socket.send(response_data.encode('iso-8859-1'))

                    pprint(Request_Line)
                    pprint(header)
                else:
                    pass
                
                # read body
            fd.close()

    
    def route(self, path, methods=['GET']):
        def wrap(func):
            self.routearr.append({
                'path': path,
                'methods': methods,
                'handler': func,
            })
            return func
        return wrap 

    def basic_auth(self, id, password):
        def wrap(func):
            self.routearr.append({
                'path': id,
                'methods': password,
            })
            return func
        return wrap