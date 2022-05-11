from enum import Enum, auto
from io import BytesIO

from parser import is_char, is_ctl, is_digit, is_token


stream = BytesIO(b"post /a/b/c/d/e?foo=bar&asd=asdf#id-123 HTTP/10.1\r\n")
stream = BytesIO(b"post /a/b/c/d/e?asdj=bdss#id-123 HTTP/10.1\r\n")

# FSM

class ParserState(Enum):
    Method = auto()
    RequestURI = auto()
    Version = auto()

def parse_http_request_line(stream):
    state = ParserState.Method
    method = ''
    uri = ''
    version = ''

    while True:
        octet = stream.read(1).decode('iso-8859-1')
        if len(octet) == 0:
            return method, uri, version

        if state == ParserState.Method:
            if is_token(octet):
                method += octet
            elif octet == ' ':
                state = ParserState.RequestURI
            else:
                raise ValueError('invalid http msg')
        elif state == ParserState.RequestURI:
            if is_char(octet) and not (ord(octet) <= 32):
                uri += octet
            elif octet == ' ':
                # validation !
                state = ParserState.Version
        elif state == ParserState.Version:
            word = octet + stream.read(4).decode('iso-8859-1')
            if word == 'HTTP/':
                # ok
                version += word
                sub_ver_flag = False
                while True:
                    octet = stream.read(1).decode('iso-8859-1')
                    if is_digit(octet):
                        version += octet
                    elif octet == '.' and not sub_ver_flag:
                        sub_ver_flag = True
                        version += octet
                    elif sub_ver_flag and octet == '\r':
                        octet = stream.read(1).decode('iso-8859-1')
                        if octet == '\n':
                            return method, uri, version
                        else:
                            raise ValueError('invalid version')
                    else:
                        raise ValueError('invalid version')
            else:
                raise ValueError('invalid version')



print(parse_http_request_line(stream))
