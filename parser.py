from urllib.parse import urlparse
'''
    CHAR           = <any US-ASCII character (octets 0 - 127)>
    UPALPHA        = <any US-ASCII uppercase letter "A".."Z">
    LOALPHA        = <any US-ASCII lowercase letter "a".."z">
    ALPHA          = UPALPHA | LOALPHA
    DIGIT          = <any US-ASCII digit "0".."9">
    CTL            = <any US-ASCII control character (octets 0 - 31) and DEL (127)>
    LWS            = [CRLF] 1*( SP | HT )
    TEXT           = <any OCTET except CTLs, 
                     but including LWS>
    word           = token | quoted-string
        token          = 1*<any CHAR except CTLs or tspecials>

       tspecials      = "(" | ")" | "<" | ">" | "@"
                      | "," | ";" | ":" | "\" | <">
                      | "/" | "[" | "]" | "?" | "="
                      | "{" | "}" | SP | HT

        quoted-string  = ( <"> *(qdtext) <"> )

       qdtext         = <any CHAR except <"> and CTLs,
                        but including LWS>
'''

def is_char(octet):
    if len(octet) > 1:
        return False
    return 0 <= ord(octet) <= 127

def is_upalpha(octet):
    if len(octet) > 1:
        return False
    return 65 <= ord(octet) < 91

def is_loalpha(octet):
    if len(octet) > 1:
        return False
    return 97 <= ord(octet) < 123

def is_alpha(octet):
    if len(octet) > 1:
        return False
    return is_upalpha(octet) or is_loalpha(octet)

def is_digit(octet):
    if len(octet) > 1:
        return False    
    return 48 <= ord(octet) < 58

def is_ctl(octet):
    if len(octet) > 1:
        return False    
    return 0 <= ord(octet) < 32 or ord(octet) == 127

def is_ht(octet):
    if len(octet) > 1:
        return False    
    return ord(octet) == 9

def is_sp(octet):
    if len(octet) > 1:
        return False    
    return ord(octet) == 32

# 
def is_lws(octet):
    # a="123"
    # a.startswith(prefix) / strip
    if '\r\n' in octet:
        octet = octet[2:]
    for oct in octet:
        if not(is_ht(oct) or is_sp(oct)):
            return False
    return True

def is_text(octet):
    if is_ctl(octet):
        return is_lws(octet)
    return True

def is_word(octet):
    return is_token(octet) or is_quoted_string(octet)


def is_token(octet):
    if len(octet) ==0:
        return False
    for oct in octet:
        if is_ctl(oct) or is_tspecials(oct):
            return False
    return True

def is_tspecials(octet):
    if len(octet) > 1:
        return False
    tspecials = ["(", ")", "<", ">", "@"\
            , ",", ";", ":", "\\", "\""\
            , "/", "[", "]", "?", "="\
           , "{", "}", "\t", " "]
    for tspecial in tspecials:
        if ord(tspecial) == ord(octet):
            return True
    return False

# 
def is_quoted_string(octet):
    if (ord(octet[0]) ,ord(octet[-1])) == (34, 34):
        octet_arr = octet[1:-1]
        word = ""
        for octet in octet_arr:
            word +=octet
            if word in ("\r", "\r\n"):
                continue
            if is_qdtext(word):
                word = ""
                continue
            else:
                return False
        return True
    return False
    

def is_qdtext(octet):
    if is_lws(octet): #\r\n\t
        return True

    if len(octet) > 1:
        return False
    
    if ord(octet) == 34 or is_ctl(octet): # ""
        return False

    return is_char(octet)

'''
    HTTP-Version   = "HTTP" "/" 1*DIGIT "." 1*DIGIT
    URI            = ( absoluteURI | relativeURI ) [ "#" fragment ]

    absoluteURI    = scheme ":" *( uchar | reserved )

    relativeURI    = net_path | abs_path | rel_path

    net_path       = "//" net_loc [ abs_path ]
    abs_path       = "/" rel_path
    rel_path       = [ path ] [ ";" params ] [ "?" query ]

    path           = fsegment *( "/" segment )
    fsegment       = 1*pchar
    segment        = *pchar

    params         = param *( ";" param )
    param          = *( pchar | "/" )

    scheme         = 1*( ALPHA | DIGIT | "+" | "-" | "." )
    net_loc        = *( pchar | ";" | "?" )
    query          = *( uchar | reserved )
    fragment       = *( uchar | reserved )

    pchar          = uchar | ":" | "@" | "&" | "=" | "+"
    uchar          = unreserved | escape
    unreserved     = ALPHA | DIGIT | safe | extra | national

    escape         = "%" HEX HEX
    reserved       = ";" | "/" | "?" | ":" | "@" | "&" | "=" | "+"
    extra          = "!" | "*" | "'" | "(" | ")" | ","
    safe           = "$" | "-" | "_" | "."
    unsafe         = CTL | SP | <"> | "#" | "%" | "<" | ">"
    national    = <any OCTET excluding ALPHA, DIGIT, reserved, extra, 
                     safe, and unsafe>
'''

def is_HTTP_Version(octet):
    if octet[0:5] != "HTTP/":
        return False
    if octet.count(".") > 1:
        return False
    if octet.find(".") == 5:
        return False
    for i in range(5, octet.find(".")): 
        if is_digit(octet[i]) == False:
            return False
    for i in range(octet.find(".")+1,  len(octet)):
        if is_digit(octet[i]) == False:
            return False
    return True
    
def is_safe(octet):
    if octet > 1:
        return False
    safes = ["$" | "-" | "_" | "."]
    for safe in safes:
        if ord(octet) == ord(safe):
            return True
    return False

def is_unsafe(octet):
    if octet > 1:
        return False
    if is_ctl(octet):
        return True
    un_safes = ["\t", "\"", "#", "%", "<", ">"]
    for un_safe in un_safes:
        if ord(octet) == ord(un_safe):
            return True
    return False

def is_extra(octet):
    if octet > 1:
        return False
    extras = ["!", "*", "'", "(", ")", ","]
    for extra in extras:
        if ord(octet) == ord(extra):
            return True
    return False

def is_reserved(octet):
    if octet > 1:
        return False
    reserveds = [";", "/", "?", ":", "@", "&", "=", "+"]
    for reserved in reserveds:
        if ord(octet) == ord(reserved):
            return True
    return False

# def is_national(octet):
#     is

def is_Method(octet):
    Methods = ["GET", "HEAD", "POST"]
    if is_token(octet):
        return True
    for Method in Methods:
        if octet == Method:
            return octet
    return False

def is_Request_URI(octet):
    url = urlparse(octet)
    if url.scheme == "" :
        return False
    return True
    
def is_Request_Line(octet):
    if octet[-2:] != "\r\n":
        return False
    octet = octet.split()
    if len(octet) != 3:
        return False
    print(is_Method(octet[0]))
    print(is_Request_URI(octet[1]))
    print(is_HTTP_Version(octet[2]))
    return is_Method(octet[0]) and is_Request_URI(octet[1]) and is_HTTP_Version(octet[2])
        
