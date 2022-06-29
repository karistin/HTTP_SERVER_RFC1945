import socket
import threading
import queue
from contextlib import closing
from contents import NOT_FOUND_PAGE
from handler import handler, mk_Response
from datetime import datetime
from pprint import pprint
from enum import auto
import base64


class Server():

    def __init__(self):
        self.routearr = []
        self.www_auth = {}

    def run(self, ip, port):
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as server_socket:

            server_socket.bind((ip, port))
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.listen(5)

            while True:
                client_socket, addr = server_socket.accept()
                # with closing(client_socket):
                # request_queue = queue.Queue(maxsize= 5)
                # request_queue.put(client_socket)

                # def A():
                #     q = request_queue.get()
                #     while q:
                #         Server_network(self.routearr, self.www_auth, q).start()
                #     print(request_queue)
                #     print(thread_pool)
                # thread_pool = [threading.Thread(target= A) for _ in range(10)]
                # [t.start() for t in thread_pool]

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

                with closing(client_socket):
                    # request_queue.append(Server_network(self.routearr, self.www_auth, client_socket))
                    t1 = Server_network(self.routearr, self.www_auth, client_socket)
                    # thread_pool.append(t1)
                    # if request_queue None:
                    #     request_queue.append
                    t1.start()

                # thread stop

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
            self.www_auth = {
                'id': id,
                'password': password,
            }
            return func
        return wrap


class Server_network(threading.Thread):

    def __init__(self, routerarr, www_auth, client_socket):
        threading.Thread.__init__(self)
        self.routearr = routerarr
        self.www_auth = www_auth
        self.client_socket = client_socket
        self.status_code_definitons = {
            200: 'ok',
            401: 'Unauthorized'
        }
        self.Request = {
            'Request_Line': auto(),
            'Request_headers': auto(),
            'Request_body': auto()
        }
        self.Response = {
            'Response_Status_Line': auto(),
            'Response_headers': auto(),
            'Response_body': auto()
        }
        self.Request['Request_Line'] = dict()
        self.Request['Request_headers'] = dict()
        self.Response['Response_Status_Line'] = dict()
        self.Response['Response_headers'] = dict()

        self.server_name = "ksj_server"
        # https://bobbyhadz.com/blog/python-typeerror-type-object-does-not-support-item-assignment

    def run(self):
        fd = self.client_socket.makefile(mode='rw')
        with closing(fd):

            try:
                self.Request['Request_Line'], self.Request['Request_headers'] = handler(fd)

                self.router_search(fd)

                self.response_msg()

                Res_msg = mk_Response(self.Response)
                fd.write(Res_msg)
                print('====================================================================')
            except ValueError:
                print('invaild http msg')

    def router_search(self, fd):
        for routear in self.routearr:
            if routear['path'] == self.Request['Request_Line']['path'].path and\
                    self.Request['Request_Line']['method'] in routear['methods']:

                self.Response['Response_Status_Line']['status_code'], self.Request['Request_headers'],\
                    self.Response['Response_body'], self.Request['Request_body']\
                    = routear['handler'](self.Request['Request_headers'], fd)

                pprint(self.Request)

                break
                # prevent duplicate method  
            else:
                self.Response['Response_Status_Line']['status_code'] = 404
                self.Response['Response_body'] = NOT_FOUND_PAGE

    def response_msg(self):
        self.Response['Response_Status_Line']['version'] = self.Request['Request_Line']['version']
        self.Response['Response_Status_Line']['Reason'] = self.status_code_definitons.get(
            self.Response['Response_Status_Line']['status_code'])

        self.Response['Response_headers']['Content-Type'] = 'text/html;charset=ISO-8859-1'
        self.Response['Response_headers']['Server'] = self.server_name
        self.Response['Response_headers']['Date'] = datetime.now().strftime('%a, %d %b %Y %H:%M:%S KST')
        self.check_auth()
    
    def check_auth(self):
        if self.Request['Request_headers'].get('Authorization'):
            serect = self.Request['Request_headers'].get('Authorization')
            auth = '{0}:{1}'.format(self.www_auth.get('id'), self.www_auth.get('password'))
            auth = base64.b64encode(auth.encode('ascii'))
            auth = auth.decode('utf-8')
            if serect == 'Basic {0}'.format(auth):
                self.Response['Response_Status_Line']['status_code'] = 200
                self.Response['Response_Status_Line']['Reason'] = 'ok'
        if self.Request['Request_Line']['path'].path == '/auth':
            self.Response['Response_headers']['WWW-Authenticate'] = 'Basic realm="WallyWorld"'