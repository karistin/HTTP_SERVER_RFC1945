#!/usr/bin/env python

import logging
from contents import MAIN_PAGE, NOT_FOUND_PAGE, POST_PAGE
from server import Server
from base64 import b64decode


server = Server()

#  Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ==
@server.route('/auth')
@server.basic_auth('Aladdin', 'open sesame')
def auth(headers, stream):
    print('auth')
    if 'Authorization' in headers.keys():
        value = headers['Authorization']
        if value.startswith('Basic'):
            value.lstrip('Basic')
            print(b64decode(value))
    return 200, headers, 'hello world'

@server.route('/')
def index(headers, stream):
    return 200, headers, MAIN_PAGE


@server.route('/post', methods=['POST'])
def index(headers, stream):
    print('post')
    size = int(headers.get('content-length', '0'))
    print(headers)
    body = b''
    while size > 0:
        read_size = min(4096, size)
        body += stream.read(read_size)
        size -= read_size
    body = body.decode('iso-8859-1')
    return 200, headers, POST_PAGE


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    server.run('localhost', 8081)

# netstat -nap | grep 8080
#  fuser -k -n tcp 8080