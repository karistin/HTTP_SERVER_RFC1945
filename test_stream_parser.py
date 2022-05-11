from io import BytesIO
import unittest


def parse_request_line_bytes(b):
    return parse_http_request_line(BytesIO(b))

def parse_response_line_bytes(b):
    return parse_response_line_bytes(BytesIO(b))


class TestStreamParser(unittest.TestCase):
    def test_simple_request_line(self):
        self.assertEqual(
            parse_request_line_bytes(b'GET / HTTP/1.1\r\n'),
            ('GET', '/', 'HTTP/1.1'),
        )
        self.assertEqual(
            parse_request_line_bytes(b'GET https://www.naver.com HTTP/1.1\r\n'),
            ('GET', 'https://www.naver.com', 'HTTP/1.1'),
        )

        self.assertEqual(
            parse_request_line_bytes(
                b'post /a/b/c/d/e?foo=bar&foo2=bar2#id-123 HTTP/10.1\r\n'
            ),
            ('post', '/a/b/c/d/e?foo=bar&foo2=bar2#id-123', 'HTTP/10.1'),
        )

        with self.assertRaises(ValueError):
            parse_request_line_bytes(
                b'p\0ost / HTTP/10.1\r\n'
            )

        with self.assertRaises(ValueError):
            parse_request_line_bytes(
                b'p@ost / HTTP/10.1\r\n'
            )

        with self.assertRaises(ValueError):
            parse_request_line_bytes(
                b'get / HTTP/1.0.1\r\n'
            )

        with self.assertRaises(ValueError):
            parse_request_line_bytes(
                b'GET / HTTP/1.1\n'
            )

        with self.assertRaises(ValueError):
            parse_request_line_bytes(
                b'GET / HTTP/1.1'
            )

        with self.assertRaises(ValueError):
            parse_request_line_bytes(
                b'GET  /  HTTP/1.1'
            )

        with self.assertRaises(ValueError):
            parse_request_line_bytes(
                b'GET /  HTTP/1.1'
            )

        with self.assertRaises(ValueError):
            parse_request_line_bytes(
                b'GET foo/bar  HTTP/1.1'
            )

    def test_full_request_line(self):
        payload = b"""POST / HTTP/1.1

Accept: text/html,application/xhtml+xml
Accept-Language: en-US,en;q=0.9,ko-KR;q=0.8
User-Agent: Mozilla/5.0
Content-Type: application/x-www-form-urlencoded
Content-Length: 19

foo=hello&bar=world"""
        self.assertEqual(
            parse_request_line_bytes(payload),
            ('GET', '/', 'HTTP/1.1', {
                'Accept': 'text/html,application/xhtml+xml',
                'Accept-Language': 'en-US,en;q=0.9,ko-KR;q=0.8',
                'User-Agent': 'Mozilla/5.0',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Content-Length': '19',
            }, 'foo=hello&bar=world'),
        )

    def test_full_response_line(self):
        payload = b"""HTTP/1.1 200 OK

Date: Wed, 11 May 2022 20:14:00 GMT
Server: PyServer/5.0
Content-Type: text/plain
Content-Length: 11

hello world"""
        self.assertEqual(
            parse_response_line_bytes(payload),
            ('HTTP/1.1', '200', 'OK', {
                'Date': 'Wed, 11 May 2022 20:14:00 GMT',
                'Server': 'PyServer/5.0',
                'Content-Type': 'text/plain',
                'Content-Length': '11',
            }, 'hello world'),
        )
