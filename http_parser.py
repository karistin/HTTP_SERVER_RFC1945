from enum import Enum, auto
from io import BytesIO
from time import sleep
from urllib.parse import urlparse
from parser import is_token, is_char, is_ctl, is_sp, is_digit,\
    is_text, is_lws, is_scheme, is_netloc, is_path, is_query, \
    is_param, is_fragment
import json
from pprint import pprint
class ParserState(Enum):
    Method = auto()
    RequestURI = auto()
    Version = auto()
    Status = auto()
    Reason = auto()
    Header = auto()
    Body = auto()    


stream = (b"""POST http://www.naver.com/index.html;params;params2?query#fragment HTTP/1.1
Accept: text/html,application/xhtml+xml
Accept-Language: en-US,en;q=0.9,ko-KR;q=0.8
User-Agent: Mozilla/5.0
Content-Type: application/x-www-form-urlencoded
Content-Length: 19

foo=hello&bar=world"""
)

stream2 =  b"""HTTP/1.1 302 Moved Temporarily
Connection: close
Content-Type: text/html
Date: Tue, 31 May 2022 05:56:07 GMT
Location: https://www.naver.com/
Server: NWS

<html>
<head><title>302 Found</title></head>
<body>
<center><h1>302 Found</h1></center>
<hr><center> NWS </center>
</body>
</html>"""


def http_Full_Request_parser(stream):
    stream = b'\r\n'.join(stream.split(b'\n'))
    stream = BytesIO(stream)
    # something?
    state = ParserState.Method
    Request_Line = {'method' : "", 'uri' : "", 'version' : ""}
    header = {}
    body = ''
    field_name = ""
    field_value = ""
# Request-Line = Method SP Request-URI SP HTTP-Version CRLF
    while True:
        try:
            octet = stream.read(1).decode('iso-8859-1')
            # read full_request 
            if len(octet) == 0:
                return Request_Line, header, body
                # nothing ?
            if state == ParserState.Method:
                if is_token(octet):
                    Request_Line['method'] += octet
                elif octet == ' ':
                    state = ParserState.RequestURI
                else:
                    raise ValueError('invalid http msg')
            elif state == ParserState.RequestURI:
                if is_char(octet) and not is_ctl(octet) and not is_sp(octet):
                        Request_Line['uri'] += octet
                elif octet == ' ':
                    uri = urlparse(Request_Line['uri'])
                    # absoulte uri
                    # scheme : netloc 
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
                    Request_Line['uri'] = uri
                    # Request_Line['uri'] = uri.geturl()
                    state = ParserState.Version

            elif state == ParserState.Version:
                version = octet + stream.read(4).decode('iso-8859-1')
                if version == 'HTTP/':
                    Request_Line['version'] += version
                    sub_ver_flag = False
                    while True:
                        octet = stream.read(1).decode('iso-8859-1')
                        # HTTP Version
                        if is_digit(octet):
                            Request_Line['version'] += octet
                        elif octet == '.' and not sub_ver_flag:
                            sub_ver_flag = True
                            Request_Line['version'] += octet
                        elif sub_ver_flag and octet == '\r':
                            octet = stream.read(1).decode('iso-8859-1')
                            if octet == '\n':
                                state = ParserState.Header
                                sub_ver_flag == True
                                break
                            else:
                                raise ValueError('invalid version')
            elif state == ParserState.Header:
                if sub_ver_flag == True:
                    if octet == ":":
                        sub_ver_flag = False
                        octet = stream.read(1).decode('iso-8859-1')
                        continue
                    if octet == "\r":
                        state = ParserState.Body
                        continue
                    if not is_token(octet):
                        raise ValueError("invalid http msg")
                    field_name += octet
                elif sub_ver_flag == False:
                    if octet in (" ", ":"):
                        octet = stream.read(1).decode('iso-8859-1')
                        continue
                    if octet == '\r':
                        octet = stream.read(1).decode('iso-8859-1')
                        if octet == '\n':
                            sub_ver_flag = True
                            header[field_name] = field_value
                            field_name = ""
                            field_value = ""
                            continue
                    if is_ctl(octet):
                        if not is_lws(octet):
                            raise ValueError("invalid http msg")
                    if is_char(octet):
                        field_value += octet
            elif state == ParserState.Body:
                body += octet
        except EOFError:
            return Request_Line, header, body



# Full-Response   = Status-Line             ; Section 6.1
#                     *( General-Header       ; Section 4.3
#                     | Response-Header      ; Section 6.2
#                     | Entity-Header )      ; Section 7.1
#                     CRLF
#                     [ Entity-Body ]         ; Section 7.2
# Status-Line = HTTP-Version SP Status-Code SP Reason-Phrase CRLF

def http_Full_Response_parser(stream):
    stream = b'\r\n'.join(stream.split(b'\n'))
    stream = BytesIO(stream)
    state = ParserState.Version
    Status_Line = {'version' : "", 'status_code' : "", 'Reason_Phrase' : ""}
    header = {}
    body = ''
    field_name = ""
    field_value = ""
    sub_ver_flag = True
    while True:
        try:
            octet = stream.read(1).decode('iso-8859-1')
            # read full_request 
            if len(octet) == 0:
                return Status_Line, header, body
            if state == ParserState.Version:
                version = octet + stream.read(4).decode('iso-8859-1')
                if version == 'HTTP/':
                    Status_Line['version'] += version
                    sub_ver_flag = False
                    while True:
                        octet = stream.read(1).decode('iso-8859-1')
                        # HTTP Version
                        if is_digit(octet):
                            Status_Line['version'] += octet
                        elif octet == '.' and not sub_ver_flag:
                            sub_ver_flag = True
                            Status_Line['version'] += octet
                        elif sub_ver_flag and octet == ' ':
                                state = ParserState.Status
                                break
                        else:
                            raise ValueError('invalid version')
            elif state == ParserState.Status:
                if octet == ' ':
                    state = ParserState.Reason
                    if len(Status_Line['status_code']) != 3:
                        raise ValueError('invalid status')
                    continue
                if not is_digit(octet):
                    raise ValueError('invalid status')
                Status_Line['status_code'] += octet
            elif state == ParserState.Reason:
                if octet == '\r':
                    octet = stream.read(1).decode('iso-8859-1')
                    if octet == '\n':
                        state = ParserState.Header
                        continue
                if not is_text(octet):
                    return ValueError('invalid Reason')
                Status_Line['Reason_Phrase'] += octet

            elif state == ParserState.Header:
                if sub_ver_flag == True:
                    if octet == ":":
                        sub_ver_flag = False
                        octet = stream.read(1).decode('iso-8859-1')
                        continue
                    if octet == "\r":
                        state = ParserState.Body
                        continue
                    if not is_token(octet):
                        raise ValueError("invalid http msg")
                    field_name += octet
                elif sub_ver_flag == False:
                    if octet in (" ", ":"):
                        octet = stream.read(1).decode('iso-8859-1')
                        continue
                    if octet == '\r':
                        octet = stream.read(1).decode('iso-8859-1')
                        if octet == '\n':
                            sub_ver_flag = True
                            header[field_name] = field_value
                            field_name = ""
                            field_value = ""
                            continue
                    if is_ctl(octet):
                        if not is_lws(octet):
                            raise ValueError("invalid http msg")
                    if is_char(octet):
                        field_value += octet
            elif state == ParserState.Body:
                body += octet
        except EOFError:
            return Status_Line

(Request_Line, header, body) = (http_Full_Request_parser(stream))


# pprint(Request_Line)
# pprint(header)
# pprint(body)

(Response_Line, header, body) = http_Full_Response_parser(stream2)

pprint(Response_Line)
pprint(header)
pprint(body)
