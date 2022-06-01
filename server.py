from html.entities import html5
import socket
from datetime import datetime
from http_parser import http_Full_Request_parser
from pprint import pprint
from sys import argv

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if len(argv) == 1:
    raise ValueError("invaild option")
server_socket.bind(('localhost', int(argv[1])))
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.listen(0)

mainpage = '''
<html>
<head><title>200 OK</title></head>
<body>
<center><h1>200 OK</h1></center>
<hr><center> Python Server </center> 
</body>
</html>
'''

servepage = '''
<html>
<head><title>200 OK</title></head>
<body>
<center><h1>200 OK</h1></center>
<div>Hello world</div>
</body>
</html>
'''

NotFoundpage = '''
<html>
<head><title>404 Not Found</title></head>
<body>
404 Not Found 
</body>
</html>
'''

# HTTP/1.1 200 OK
# Cache-Control: private, max-age=0
# Content-Encoding: gzip
# Content-Length: 6404
# Content-Type: text/html; charset=ISO-8859-1
# Date: Wed, 01 Jun 2022 11:35:48 GMT
# Expires: -1
# P3P: CP="This is not a P3P policy! See g.co/p3phelp for more info."
# Server: gws
# Set-Cookie: 1P_JAR=2022-06-01-11; expires=Fri, 01-Jul-2022 11:35:48 GMT; path=/; domain=.google.com; Secure
# Set-Cookie: AEC=AakniGMUlxOPDsJ0MgZC1h1YMbiqBG50vaVlsAkLDyzaFAf3wrynp6mTaA; expires=Mon, 28-Nov-2022 11:35:48 GMT; path=/; domain=.google.com; Secure; HttpOnly; SameSite=lax
# Set-Cookie: NID=511=pZRprqiprXE9w8h4CQeQYncPCXhjImovjveQAFc8d3zloBZOp9On1FQ84X6dcM0ZqohqnuBGBuG2da_Vhyn3854ab3SJq-EAQ3gxwUhCggDv3j0Gpi3bxO9QTbyB5jOYFx3acW9Jzb8ZfZQ2euVt_1Xv2uCMd7nhfoJWKuDNxO8; expires=Thu, 01-Dec-2022 11:35:48 GMT; path=/; domain=.google.com; HttpOnly
# X-Frame-Options: SAMEORIGIN
# X-XSS-Protection: 0

# Request_Line = {'method' : "", 'uri' : "", 'version' : ""}


while True:
    try:
        print("===================================")
        client_socket, addr = server_socket.accept()
        data = client_socket.recv(65535)
        try:
            (Request_Line, header, body) = (http_Full_Request_parser(data))
        except ValueError:
            client_socket.send("Invalid http msg".encode())
            client_socket.close()
        
        pprint(Request_Line)
        pprint(header)
        pprint("body :"+body)

        server_name = "Python Server"

        if Request_Line['method'] == "GET":
            response_data = "{0} 200 OK\r\nContent-Length: {1}\r\nContent-Type: text/html; charset=ISO-8859-1\r\nServer: {2}\r\nDate: {3}\r\n".format(\
            Request_Line['version'], len(data), server_name, 
            datetime.now().strftime('%a, %d %b %Y %H:%M:%S KST'))
            if Request_Line['uri'].path == "/":
                response_data += "\r\n" + mainpage
            elif Request_Line['uri'].path == "/serve":
                response_data += "\r\n" + servepage
            else:
                response_data += "\r\n" + NotFoundpage
        else:
            response_data = "{0} 405 Method Not Allowed\nServer: {1}\nDate: {2}\n".format(Request_Line['version'], server_name, 
            datetime.now().strftime('%a, %d %b %Y %H:%M:%S KST'))
            response_data += "\r\n" + NotFoundpage

        client_socket.send(response_data.encode())
        client_socket.close()

    except KeyboardInterrupt:
        client_socket.close()
        exit(1)
