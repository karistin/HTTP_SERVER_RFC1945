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
    if '\r\n' in octet:
        octet = octet.strip('\r\n')
    return is_ht(octet) or is_sp(octet)

def is_text(octet):
    if is_lws(octet):
        return True
    if is_ctl(octet):
        return False
    return True

def is_word(octet):
    if is_token(octet) or is_quoted_string(octet):
        return True
    return False

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
    if ord(octet[0]) == 34 and ord(octet[len(octet)-1]) == 34:
        octet_arr = octet[1:len(octet)-1]
        if len(octet_arr) == 0:
            return True
        for octet in octet_arr:
            if is_qdtext(octet):
                continue
            else:
                return False
        return True
    return False

def is_qdtext(octet):
    if ord(octet) == 34:
        return False
    return is_text(octet)