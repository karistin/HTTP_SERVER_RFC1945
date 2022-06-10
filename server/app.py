import logging
import base64
from contents import MAIN_PAGE, NOT_FOUND_PAGE, POST_PAGE
from server import Server #, basic_auth


server = Server()

# @server.route('/auth')
# @basic_auth('Aladdin', 'open sesame')
# def auth(headers, stream):
#     return 200, {}, b'hello world'

@server.route('/')
def index(headers, stream):
    return 200, {}, MAIN_PAGE.encode('iso-8859-1')


# @server.route('/post', methods=['POST'])
# def index(headers, stream):
#     print('post')
#     size = int(headers.get('content-length', '0'))
#     body = b''
#     while size > 0:
#         read_size = min(4096, size)
#         body += stream.read(read_size)
#         size -= read_size
#     body = body.decode('iso-8859-1')
#     return 200, {}, POST_PAGE.format(body).encode('iso-8859-1')


if __name__ == '__main__':
    # logging.basicConfig(encoding='utf-8', level=logging.DEBUG)
    server.run('localhost', 8080)

# netstat -nap | grep 8080
#  fuser -k -n tcp 8080