from parser import is_token, is_char, is_text, is_tspecials, is_qdtext, is_lws, is_ctl
from io import BytesIO


stream = b'\r\n'.join([
    b'Accept: text/html,application/xhtml+xml',
    b'Accept-Language: en-US,en;q=0.9,ko-KR;q=0.8',
    b'User-Agent: 0Mozilla/5.0',
    b'Content-Type: application/x-www-form-urlencoded',
    b'Content-Length: 19'
]
)


    #    HTTP-header    = field-name ":" [ field-value ] CRLF

    #    field-name     = token
    #    field-value    = *( field-content | LWS )

    #    field-content  = <the OCTETs making up the field-value
    #                     and consisting of either *TEXT or combinations
    #                     of token, tspecials, and quoted-string>

stream = BytesIO(stream)
buf = stream.read(1).decode('iso-8859-1')
state = 1
header = {}
field_name = ""
field_value = ""


while len(buf) != 0:
    if state == 1:
        if buf == ":":
            state = 2 
            continue
        if not is_token(buf):
            raise ValueError('not token')
        field_name += buf
    elif state == 2:
        if buf in (" ", ":"):
            buf = stream.read(1).decode('iso-8859-1')
            continue
        if buf == "\r":
            buf = stream.read(1).decode('iso-8859-1')
            if buf == "\n":
                state = 1
                header[field_name] = field_value 
                field_name = ""
                field_value = ""
                buf = stream.read(1).decode('iso-8859-1') 
                continue
        if is_ctl(buf):
            if not is_lws(buf):
                raise ValueError("value")
        if is_char(buf):
            field_value += buf
    buf = stream.read(1).decode('iso-8859-1')

print(header)