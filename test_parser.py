import unittest
from parser import is_char, is_upalpha, is_loalpha, is_alpha, \
    is_digit, is_ctl, is_ht, is_sp, is_lws, is_text, is_word, \
    is_token, is_tspecials, is_quoted_string, is_qdtext, is_HTTP_Version, \
    is_safe, is_unsafe, is_extra, is_reserved, is_national, is_escape, is_uchar, \
    is_absoluteURI, is_relativeURI, is_scheme

class TestParser(unittest.TestCase):
    def test_is_char(self):
        self.assertTrue(is_char("s"))
        self.assertTrue(is_char("a"))
        self.assertTrue(is_char("e"))

        self.assertFalse(is_char("\x80"))
        self.assertFalse(is_char("as"))
        self.assertFalse(is_char("\xf0"))
    
    def test_is_upalpha(self):
        self.assertTrue(is_upalpha("A"))
        self.assertTrue(is_upalpha("S"))
        self.assertTrue(is_upalpha("Z"))

        self.assertFalse(is_upalpha("\0"))
        self.assertFalse(is_upalpha("a"))
        self.assertFalse(is_upalpha("z"))
        self.assertFalse(is_upalpha("AZ"))
    
    def test_is_loalpha(self):
        self.assertTrue(is_loalpha('a'))
        self.assertTrue(is_loalpha('c'))
        self.assertTrue(is_loalpha('s'))

        self.assertFalse(is_loalpha('D'))
        self.assertFalse(is_loalpha('S'))
        self.assertFalse(is_loalpha('K'))
        self.assertFalse(is_loalpha("az"))

    def test_is_alpha(self):
        self.assertTrue(is_alpha('e'))
        self.assertTrue(is_alpha('c'))
        self.assertTrue(is_alpha('r'))

        self.assertFalse(is_alpha('2'))
        self.assertFalse(is_alpha('ab'))
        self.assertFalse(is_alpha('\x7f'))
        self.assertFalse(is_alpha('\x20'))

    def test_is_digit(self):
        self.assertTrue(is_digit('1'))
        self.assertTrue(is_digit('2'))
        self.assertTrue(is_digit('3'))

        self.assertFalse(is_digit('03'))
        self.assertFalse(is_digit('a'))
        self.assertFalse(is_digit('\x7f'))
        self.assertFalse(is_digit('\x20'))

    def test_is_ctl(self):
        self.assertTrue(is_ctl('\x12'))
        self.assertTrue(is_ctl('\x13'))
        self.assertTrue(is_ctl('\x1c'))

        self.assertFalse(is_ctl('2'))
        self.assertFalse(is_ctl('D'))
        self.assertFalse(is_ctl('\x39'))

    def test_is_lws(self):
        self.assertTrue(is_lws('\r\n'))
        self.assertTrue(is_lws(' '))
        self.assertTrue(is_lws('\t'))
        self.assertTrue(is_lws('\r\n\t'))
        self.assertTrue(is_lws('\r\n\t\t\t\t'))
        self.assertTrue(is_lws('\r\n                 '))
        
        self.assertFalse(is_lws('\r\n \r\n'))
        self.assertFalse(is_lws('2'))
        self.assertFalse(is_lws('R'))
        self.assertFalse(is_lws('\r'))
        self.assertFalse(is_lws('\n'))

    def test_is_text(self):
        self.assertTrue(is_text('\xf0'))
        self.assertTrue(is_text('\x82'))
        self.assertTrue(is_text('!'))
        self.assertTrue(is_text('@'))
        self.assertTrue(is_text('e'))
        self.assertTrue(is_text('\x32'))
        self.assertTrue(is_text('3'))
        # self.assertTrue(is_text('\r\n'))
        self.assertTrue(is_text('\t'))

        self.assertFalse(is_text('\x03'))
        self.assertFalse(is_text('\r'))
        self.assertFalse(is_text('\n'))
        self.assertFalse(is_text('\x12'))
        self.assertFalse(is_text('\x1c'))

    def test_is_word(self):
        self.assertTrue(is_word('"foo bar"'))
        self.assertTrue(is_word('"foo@bar"'))
        self.assertTrue(is_word('"foo\r\n bar"'))
        self.assertTrue(is_word('foo!bar'))
        self.assertTrue(is_word('foo%bar'))
        self.assertTrue(is_word('"foo\tbar"'))

        self.assertFalse(is_word('foo\r\nbar'))
        self.assertFalse(is_word('foo bar'))
        self.assertFalse(is_word('foo@bar'))

    def test_is_token(self):
        self.assertTrue(is_token('foo'))
        self.assertTrue(is_token('bar2'))
        self.assertTrue(is_token('foo2'))
        self.assertTrue(is_token('foo%bar'))
        self.assertTrue(is_token('foo.bar'))
        self.assertTrue(is_token('foo!bar'))

        self.assertFalse(is_token('foo[bar]'))
        self.assertFalse(is_token('foo<bar>'))
        self.assertFalse(is_token('foo{bar}'))
        self.assertFalse(is_token('foo\0bar'))
        self.assertFalse(is_token('foo bar'))
        self.assertFalse(is_token('foo\tbar'))

    def test_is_tspecials(self):
        self.assertTrue(is_tspecials('<'))
        self.assertTrue(is_tspecials('}'))
        self.assertTrue(is_tspecials(';'))
        self.assertTrue(is_tspecials('\t'))
        self.assertTrue(is_tspecials(' '))

        self.assertFalse(is_tspecials('2'))
        self.assertFalse(is_tspecials('E'))
        self.assertFalse(is_tspecials('9'))

    def test_is_quoted_string(self):
        self.assertTrue(is_quoted_string('""'))
        self.assertTrue(is_quoted_string('"foo @"'))
        self.assertTrue(is_quoted_string('"foo %ac"'))
        self.assertTrue(is_quoted_string('"foo2"'))
        self.assertTrue(is_quoted_string('"foo bar 2"'))
        self.assertTrue(is_quoted_string('"3"'))
        self.assertTrue(is_quoted_string('"3\t3"'))

        # \r 13 \n 10 => ctl  /r/n/t = true 
        # self.assertTrue(is_quoted_string('"foo bar bar\r\n2"'))
        # self.assertTrue(is_quoted_string('"3\r\n3"'))
        self.assertTrue(is_quoted_string('"3\r\n foo bar"'))

        self.assertFalse(is_quoted_string('"\x7f"'))
        self.assertFalse(is_quoted_string('"0 0 \x7f"'))
        self.assertFalse(is_quoted_string('"0 0 \0"'))

    def test_is_qdtext(self):
        self.assertTrue(is_qdtext('e'))
        self.assertTrue(is_qdtext('9'))
        self.assertTrue(is_qdtext('a'))
        self.assertTrue(is_qdtext('.'))
        self.assertTrue(is_qdtext('@'))
        # self.assertTrue(is_qdtext('\r\n'))

        self.assertFalse(is_qdtext('\0'))
        self.assertFalse(is_qdtext('\r'))
        self.assertFalse(is_qdtext('\n'))
        self.assertFalse(is_qdtext('\x7f'))
        self.assertFalse(is_qdtext('\"'))

    def test_is_HTTP_Version(self):
        self.assertTrue(is_HTTP_Version("HTTP/1.0"))
        self.assertTrue(is_HTTP_Version("HTTP/0.9"))
        self.assertTrue(is_HTTP_Version("HTTP/13.18"))


        self.assertFalse(is_HTTP_Version("HTTP/ 1.0"))
        self.assertFalse(is_HTTP_Version("HTTPP/10"))
        self.assertFalse(is_HTTP_Version("HTTP/.0"))
        self.assertFalse(is_HTTP_Version("HTTP/1..0"))
        self.assertFalse(is_HTTP_Version("HTTPP/1.0\r\n"))
        self.assertFalse(is_HTTP_Version("HTTPP/1.00231"))

    def test_is_safe(self):
        self.assertTrue(is_safe("$"))
        self.assertTrue(is_safe("-"))
        self.assertTrue(is_safe("."))
        
        self.assertFalse(is_safe(";"))
        self.assertFalse(is_safe("123"))
        self.assertFalse(is_safe("sdvd"))
        self.assertFalse(is_safe("\x01"))
        self.assertFalse(is_safe("*"))

    def test_is_unsafe(self):
        self.assertTrue(is_unsafe("\x01"))
        self.assertTrue(is_unsafe("\""))
        self.assertTrue(is_unsafe("<"))
        self.assertTrue(is_unsafe("\x7F"))
        
        self.assertFalse(is_unsafe("$"))
        self.assertFalse(is_unsafe("-"))
        self.assertFalse(is_unsafe("sdvd"))
        self.assertFalse(is_unsafe("\x21"))
        self.assertFalse(is_unsafe("."))

    def test_is_extra(self):
        self.assertTrue(is_extra("!"))
        self.assertTrue(is_extra("*"))
        self.assertTrue(is_extra(","))
        self.assertTrue(is_extra("\x28"))
        
        self.assertFalse(is_extra("$"))
        self.assertFalse(is_extra("-"))
        self.assertFalse(is_extra("sdvd"))
        self.assertFalse(is_extra("."))
    
    def test_is_reserved(self):
        self.assertTrue(is_reserved(";"))
        self.assertTrue(is_reserved("?"))
        self.assertTrue(is_reserved(":"))
        self.assertTrue(is_reserved("@"))
        
        self.assertFalse(is_reserved("\x01"))
        self.assertFalse(is_reserved("-"))
        self.assertFalse(is_reserved("sdvd"))
        self.assertFalse(is_reserved("\x21"))
        self.assertFalse(is_reserved("."))

    def test_is_national(self):
        self.assertFalse(is_national("a"))
        self.assertFalse(is_national("5"))
        self.assertFalse(is_national("?"))
        self.assertFalse(is_national("!"))
        self.assertFalse(is_national("$"))
        self.assertFalse(is_national("%"))

        # what is true ?
    
    def test_is_escape(self):
        self.assertTrue(is_escape("%AE"))
        self.assertTrue(is_escape("%\x62\x63"))
        self.assertTrue(is_escape("%\x41\x42"))
        
        self.assertFalse(is_escape("%\x01\x02"))
        self.assertFalse(is_escape("\x41\x41\x42\x42"))
        self.assertFalse(is_escape("%%\x41\x42"))
        self.assertFalse(is_escape("%\x41\x42 "))
        self.assertFalse(is_escape(" %\x41\x42"))

    def test_is_scheme(self):
        self.assertTrue(is_scheme("asdf15+-"))
        self.assertTrue(is_scheme("vdsa.21vsdv--"))
        self.assertTrue(is_scheme("16513515+-+++"))
        self.assertTrue(is_scheme("cvvsdsd"))
        
        self.assertFalse(is_scheme(""))
        self.assertFalse(is_scheme(" "))
        self.assertFalse(is_scheme("\x01"))
        self.assertFalse(is_scheme("**@@@"))


    def test_is_absoluteURI(self):
        self.assertTrue(is_absoluteURI('http://www.example.com/some/path'))
        # self.assertTrue(is_absoluteURI("vdsa.21vsdv--"))
        # self.assertTrue(is_absoluteURI("16513515+-+++"))
        # self.assertTrue(is_absoluteURI("cvvsdsd"))
        
        # self.assertFalse(is_absoluteURI(""))
        # self.assertFalse(is_absoluteURI(" "))
        # self.assertFalse(is_absoluteURI("\x01"))
        # self.assertFalse(is_absoluteURI("**@@@"))
    # def test_is_URI(self):
    #     pass

"""GET / HTTP/1.1
"""
 
'''
--------------------------------------------------------
'''
"""POST / HTTP/1.1
 
Accept: text/html,application/xhtml+xml
Accept-Language: en-US,en;q=0.9,ko-KR;q=0.8
User-Agent: Mozilla/5.0
Content-Type: application/x-www-form-urlencoded
Content-Length: 19
 
foo=hello&bar=world"""