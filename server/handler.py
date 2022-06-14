from email.header import Header
from enum import Enum, auto
from parser import is_token, is_char, is_ctl, is_sp, is_digit,\
    is_text, is_lws, is_scheme, is_netloc, is_path, is_query, \
    is_param, is_fragment
from urllib.parse import urlparse
from io import BytesIO

class ParserState(Enum):
    Method = auto()
    RequestURI = auto()
    Version = auto()
    Header = auto()
    Body = auto() 

def handler(fd, state = ParserState.Method):

    Request_Line = {'method' : "", 'path' : "", 'version' : ""}
    header = {}
    sub_ver_flag = True
    field_name = ""
    field_value = ""

    while True:
        try:
            octet = fd.read(1)
            # print(octet.encode())
            if len(octet) == 0:
                raise ValueError('invalid http msg')
            
            if state == ParserState.Method:
                if is_token(octet):
                    Request_Line['method'] += octet
                elif octet == ' ':
                    state = ParserState.RequestURI
                    continue
                else:
                    raise ValueError('invalid http msg')
            
            elif state == ParserState.RequestURI:
                if is_char(octet) and not is_ctl(octet) and not is_sp(octet):
                        Request_Line['path'] += octet
                elif octet == ' ':
                    uri = urlparse(Request_Line['path'])

                    if len(uri.scheme) > 0:
                        for oct in uri.scheme:
                            if not is_scheme(oct):
                                raise ValueError("Scheme is not correct")        
                        if len(uri.netloc) > 0:
                            for oct in uri.netloc:
                                if not is_netloc(oct):
                                    raise ValueError("Netloc is not correct")
                    # abs uri
                    elif len(uri.path) > 0 and uri.path.startswith('/'):
                            for oct in uri.path:
                                if not is_path(oct):
                                    raise ValueError("Path is not correct")
                            if len(uri.params) > 0:
                                for oct in uri.params:
                                    if not is_param(oct):
                                        raise ValueError("params is not correct")
                            if len(uri.query) > 0:
                                for oct in uri.query:
                                    if not is_query(oct):
                                        raise ValueError("query is not correct")
                    else:
                        raise ValueError("uri is not exist")
                    if len(uri.fragment) > 0:
                        for oct in uri.fragment:
                            if not is_fragment(oct):
                                raise ValueError("fragment is not correct")
                    Request_Line['path'] = uri
                    # Request_Line['uri'] = uri.geturl()
                    state = ParserState.Version

            elif state == ParserState.Version:
                version = octet + fd.read(4)

                if version == 'HTTP/':
                    Request_Line['version'] += version
                    sub_ver_flag = False
                    while state == ParserState.Version:
                        octet = fd.read(1)
                        # HTTP Version

                        if is_digit(octet):
                            Request_Line['version'] += octet
                        elif octet == '.' and not sub_ver_flag:
                            sub_ver_flag = True
                            Request_Line['version'] += octet
                        elif sub_ver_flag and octet == '\r':
                            octet = fd.read(1)
                            if octet == '\n':
                                state = ParserState.Header
                                return Request_Line
                            else:
                                raise ValueError('invalid version')
                        elif octet == '\n':
                            state = ParserState.Header
                            # return Request_Line
                            # temp
                            # raise ValueError('invalid version')
            
            elif state == ParserState.Header:
                
                if sub_ver_flag == True:
                    if octet == ":":
                        sub_ver_flag = False
                        octet = fd.read(1)
                        continue
                    # if octet == "\r":
                    #     octet = fd.read(1)
                    #     if octet == "\n":
                    #         state = ParserState.Body
                    #         return header

                    if octet == '\n':
                        return Request_Line, header
                        # return header

                    if not is_token(octet):
                        raise ValueError("invalid http msg")

                    field_name += octet
                elif sub_ver_flag == False:
                    if octet in (" "):
                        octet = fd.read(1)
                        continue

                    # if octet == '\r':
                    #     octet = fd.read(1)
                    #     if octet == '\n':
                    #         sub_ver_flag = True
                    #         header[field_name] = field_value
                    #         field_name = ""
                    #         field_value = ""
                    #         continue

                    if octet == '\n':
                        header[field_name] = field_value
                        field_name = ""
                        field_value = ""
                        sub_ver_flag = True
                        continue

                    if is_ctl(octet):
                        if not is_lws(octet):
                            raise ValueError("invalid http msg")
                    if is_char(octet):
                        field_value += octet
            fd.flush()

        except KeyboardInterrupt:
            return ValueError('CTR C')

