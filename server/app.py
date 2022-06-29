#!/usr/bin/env python

import logging
from contents import MAIN_PAGE, POST_PAGE
from server import Server


server = Server()
PORT = 8082


#  http -a ksj:1109 localhost:8086/auth
#  Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ==
@server.route('/auth')
@server.basic_auth('Aladdin', 'open sesame')
def auth(headers, stream):
    return 401, headers, 'hello world', '' 


@server.route('/')
def index(headers, stream):
    return 200, headers, MAIN_PAGE, ''


@server.route('/post', methods=['POST'])
def index(headers, stream):
    size = int(headers.get('Content-Length', '0'))
    request_body = ''
    while size > 0:
        read_size = min(4096, size)
        request_body += stream.read(read_size)
        size -= read_size
    return 200, headers, POST_PAGE, request_body
# body를 읽음


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    print(f'PORT : {PORT}\r\n====================================================================')
    server.run('localhost', PORT)
