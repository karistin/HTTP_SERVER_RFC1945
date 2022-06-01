from enum import Enum, auto
from io import BytesIO
from urllib.parse import urlparse

from parser import is_char, is_ctl, is_digit, is_token,\
    is_scheme, is_netloc, is_param, is_fragment, is_query, is_path


# stream = BytesIO(b"post /a/b/c/d/e?foo=bar&asd=asdf#id-123 HTTP/10.1\r\n")
# stream = BytesIO(b"post /a/b/c/d/e?asdj=bdss#id-123 HTTP/10.1\r\n")

# FSM
# State Design Pattern
# https://ozt88.tistory.com/8

# https://datatracker.ietf.org/doc/html/rfc1945#section-5.1
# Request-Line = Method SP Request-URI SP HTTP-Version CRLF

    #    Request        = Simple-Request | Full-Request

    #    Simple-Request = "GET" SP Request-URI CRLF

    #    Full-Request   = Request-Line             ; Section 5.1
    # Request-Line = Method SP Request-URI SP HTTP-Version CRLF
    #                     *( General-Header        ; Section 4.3
    #                      | Request-Header        ; Section 5.2
    #                      | Entity-Header )       ; Section 7.1
    #                     CRLF
    #                     [ Entity-Body ]          ; Section 7.2



#  Method         = "GET"                    ; Section 8.1
#                 | "HEAD"                   ; Section 8.2
#                 | "POST"                   ; Section 8.3
#                 | extension-method(token)
# Request-URI    = absoluteURI | abs_path

class ParserState(Enum):
    Method = auto()
    RequestURI = auto()
    Version = auto()

class HeaderState(Enum):
    General = auto()
    Request = auto()
    Entity  = auto()
    Body    = auto()

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
        # 메소드 저장 부분
        elif state == ParserState.RequestURI:
            if is_char(octet):
                # if is_ctl(octet):
                #     raise ValueError('CTL in uri')
                uri += octet
            elif octet == ' ':
                # validation !
                octet = urlparse(uri)
                uri = ''
                # absoulte uri
                # scheme : netloc 
                if len(octet.scheme) > 0:
                    for oct in octet.scheme:
                        if not is_scheme(oct):
                            raise ValueError("Scheme is not correct")        
                    if len(octet.netloc) > 0:
                        for oct in octet.netloc:
                            if not is_netloc(oct):
                                raise ValueError("Netloc is not correct")
                # abs uri
                elif len(octet.path) > 0 and octet.path.startswith('/'):
                        for oct in octet.path:
                            if not is_path(oct):
                                raise ValueError("Path is not correct")
                        if len(octet.params) > 0:
                            for oct in octet.params:
                                if not is_param(oct):
                                    raise ValueError("params is not correct")
                        if len(octet.query) > 0:
                            for oct in octet.query:
                                if not is_query(oct):
                                    raise ValueError("query is not correct")
                if len(octet.fragment) > 0:
                    for oct in octet.fragment:
                        if not is_fragment(oct):
                            raise ValueError("fragment is not correct")
                if len(uri) == 0:
                    raise ValueError("uri is not exist")
                print(octet.geturl())
                uri = octet.geturl()
                state = ParserState.Version
        elif state == ParserState.Version:
            word = octet + stream.read(4).decode('iso-8859-1')
            if word == 'HTTP/':
                # ok
                version += word
                sub_ver_flag = False
                while True:
                    octet = stream.read(1).decode('iso-8859-1')
                    # HTTP Version
                    if is_digit(octet):
                        version += octet
                    elif octet == '.' and not sub_ver_flag:
                        sub_ver_flag = True
                        version += octet
                    # CRLF
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
