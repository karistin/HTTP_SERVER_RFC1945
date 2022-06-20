import socket 
import threading
from contextlib import closing
from time import sleep
from contents import NOT_FOUND_PAGE
from handler import handler, ParserState
from datetime import datetime
from pprint import pprint

status_defin ={
    200 : 'ok',
    401 : 'Unauthorized'
}

class Server():
    
    def __init__(self):
        self.routearr = []
        self.www_auth = []

    def run(self, ip, port):
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as server_socket:
           
            server_socket.bind((ip, port))
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.listen(5)

            while True:
                client_socket, addr = server_socket.accept() 
                """
                request_queue = Queue()
                thread_pool = [Thread(target=A) for _ in range(10)]
                def A():
                    while q = request_queue.pop_or_wait():
                        cli(q)
                [t.start() for t in thread_pool]
                [t.wait() for t in thread_pool]
                
                .....

                request_queue <- client_socket
                """
                t1 = threading.Thread(target=self.cli, args=(client_socket,))
                t1.start()

                # thread stop

    def cli(self, client_socket):
        with closing(client_socket):
            fd = client_socket.makefile(mode='rw')
            with closing(fd):
                Request_Line, request_headers = self.handlering(fd)
                server_name = "ksj_server"
                if True:
                # if request_headers.get('Authorization'):
                    serect = request_headers.get('Authorization')
                    print(serect)
                    if serect == "BasicWxhZGRpbjpvcGVuIHNlc2FtZQ==":
                        response_msg = '''{0} {1} {2}\r\nContent-Type: text/html;charset=ISO-8859-1\r\nServer: {3}\r\nDate: {4}\r\n'''.format(\
                        Request_Line['version'], 200,status_defin.get(200),\
                        server_name, datetime.now().strftime('%a, %d %b %Y %H:%M:%S KST'))
                        response_msg += '\r\n' + "Hello world"
                    else:
                        response_msg = '''{0} {1} {2}\r\nContent-Type: text/html;charset=ISO-8859-1\r\nServer: {3}\r\nDate: {4}\r\n'''.format(\
                        Request_Line['version'], 401,status_defin.get(401),\
                        server_name, datetime.now().strftime('%a, %d %b %Y %H:%M:%S KST'))
                        response_msg += 'WWW-Authenticate: Basic realm="WallyWorld"\r\n'
                        response_msg += '\r\n' + "Hello world"
                else:

                    status_code, response_body = self.router_search(Request_Line, request_headers, fd)

                    response_msg = self.mk_response_msg(status_code, response_body, Request_Line)
                fd.write(response_msg)

    def handlering(self, fd):
        try:
            Request_Line, request_headers = handler(fd)
        except ValueError:
            print('invaild http msg')
        return Request_Line, request_headers      

    def router_search(self, Request_Line, request_headers, fd):
        for routear in self.routearr:      
            # find correct path and method
            if routear['path'] == Request_Line['path'].path and\
                Request_Line['method'] in routear['methods']:

                status_code, header, response_body, request_body \
                = routear['handler'](request_headers, fd)
                pprint(Request_Line)
                pprint(header)
                pprint(request_body)
                print('=============================')
                break
            # can't find 
            else:
                status_code = 404
                response_body = NOT_FOUND_PAGE
        return status_code, response_body

    def mk_response_msg(self, status_code, response_body, Request_Line):

        server_name = "ksj_server"

        response_msg = '''{0} {1} {2}\r\nContent-Type: text/html;charset=ISO-8859-1\r\nServer: {3}\r\nDate: {4}\r\n'''.format(\
            Request_Line['version'], status_code,status_defin.get(status_code),\
            server_name, datetime.now().strftime('%a, %d %b %Y %H:%M:%S KST'))
        
        response_msg += '\r\n' + response_body

        return response_msg

    def auth(request_headers, response_msg):
        if request_headers.get('Authorization'):
            serect = request_headers.get('Authorization')
            print(serect)
            if serect == "Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ==":
                return 200, response_msg
            response_msg += 'WWW-Authenticate: Basic realm="WallyWorld"\r\n'
            return 401, response_msg
        return 200, response_msg

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
            self.www_auth.append({
                'path': id,
                'methods': password,
            })
            return func
        return wrap