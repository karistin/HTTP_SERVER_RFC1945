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
    print(type(stream))
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
                if is_ctl(octet):
                    raise ValueError('CTL in uri')
                uri += octet
            elif octet == ' ':
                # validation !
                octet = urlparse(uri)
                uri = ''
                # absoulte uri
                if len(octet.scheme) > 0:
                    if len(octet.netloc) > 0:
                        return True
                # abs uri
                else:
                    if len(octet.path) > 0 and path.startswith('/'):
                        if len(octet.params) > 0:
                            pass
                        if len(octet.query) > 0:
                            pass
                    else:
                        raise ValueError("1")
                if len(octet.fragment) > 0:
                    pass
                if len(octet.scheme) > 0:
                    for oct in octet.scheme:
                        if is_scheme(oct):
                            uri += oct
                        else:
                            raise ValueError('invalid scheme')
                    uri += ":"
                if len(octet.netloc) > 0:
                    uri += "//"
                    for oct in octet.netloc:
                        if is_netloc(oct):
                            uri += oct
                        else:
                            raise ValueError('invalid netloc')
                if len(octet.path) > 0:
                    for oct in octet.path:
                        if is_path(oct):
                            uri += oct
                        else:
                            raise ValueError('invalid path')
                if len(octet.params) > 0:
                    uri += ";"
                    for oct in octet.params:
                        if is_param(oct):
                            uri += oct
                        else:
                            raise ValueError('invalid params')
                if len(octet.query) > 0:
                    uri += "?"
                    for oct in octet.query:
                        if is_query(oct):
                            uri += oct
                        else:
                            raise ValueError('invalid query')
                if len(octet.fragment) > 0:
                    uri += "#"
                    for oct in octet.fragment:
                        if is_fragment(oct):
                            uri += oct
                        else:
                            raise ValueError('invalid fragment')
                if len(uri) == 0:
                    raise ValueError('uri is not exist')
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

    #    Request-Header = Authorization            ; Section 10.2
    # Authorization  = "Authorization" ":" credentials
    #                   | From                     ; Section 10.8
    # From = "From" ":" mailbox
    #                   | If-Modified-Since        ; Section 10.9
    # If-Modified-Since = "If-Modified-Since" ":" HTTP-date
    #                   | Referer                  ; Section 10.13
    #  Referer        = "Referer" ":" ( absoluteURI | relativeURI )
    #                   | User-Agent 
    # User-Agent     = "User-Agent" ":" 1*( product | comment )

def parse_response_line_bytes(steam):
    parse_http_request_line(steam)

    state = HeaderState.General
    General = ""
    Request = ""
    Entity = ""
    Body = ""
    while True:
        octet = stream.read(1).decode('iso-8859-1')
        if len(octet) == 0:
            return ""

    #    General-Header = Date                     ; Section 10.6
    # Date           = "Date" ":" HTTP-date
    #                   | Pragma                   ; Section 10.12
    #        Pragma           = "Pragma" ":" 1#pragma-directive
    #    pragma-directive = "no-cache" | extension-pragma
    #    extension-pragma = token [ "=" word ]

        if state == HeaderState.General:
            word = octet + stream.read(4).decode('iso-8859-1')
            if word == "DATE:":
                pass
            else:
                state = HeaderState.Request

        elif state == HeaderState().Request:
            pass
# print(parse_http_request_line(stream))
