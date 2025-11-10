#
# Copyright (C) 2025 pdnguyen of HCMC University of Technology VNU-HCM.
# All rights reserved.
# This file is part of the CO3093/CO3094 course.
#
# WeApRous release
#
# The authors hereby grant to Licensee personal permission to use
# and modify the Licensed Source Code for the sole purpose of studying
# while attending the course
#

"""
daemon.request
~~~~~~~~~~~~~~~~~

This module provides a Request object to manage and persist 
request settings (cookies, auth, proxies).
"""
from daemon.utils import get_auth_from_url
from .dictionary import CaseInsensitiveDict

class Request():
    """The fully mutable "class" `Request <Request>` object,
    containing the exact bytes that will be sent to the server.

    Instances are generated from a "class" `Request <Request>` object, and
    should not be instantiated manually; doing so may produce undesirable
    effects.

    Usage::

      >>> import deamon.request
      >>> req = request.Request()
      ## Incoming message obtain aka. incoming_msg
      >>> r = req.prepare(incoming_msg)
      >>> r
      <Request>
    """
    __attrs__ = [
        "method",
        "url",
        "headers",
        "body",
        "reason",
        "cookies",
        "body",
        "routes",
        "hook",
    ]

    def __init__(self):
        #: HTTP verb to send to the server.
        self.method = None
        #: HTTP URL to send the request to.
        self.url = None
        #: dictionary of HTTP headers.
        self.headers = None
        #: HTTP path
        self.path = None        
        # The cookies set used to create Cookie header
        self.cookies = None
        #: request body to send to the server.
        self.body = None
        #: Routes
        self.routes = {}
        #: Hook point for routed mapped-path
        self.hook = None

    def extract_request_line(self, request):
        """
        Tách dòng đầu tiên trong request để lấy:
        +HTTP method
        +path (đường dẫn) (Nếu / thì mặc định là /index.html)
        +version (HTTP/1.1, HTTP/2.0, …)
        Example: GET / HTTP/1.1
        => method = GET
        => path = /index.html
        => version = HTTP/1.1
        """
        try:
            lines = request.splitlines()
            first_line = lines[0]
            method, path, version = first_line.split()

            if path == '/':
                path = '/index.html'
        except Exception:
            return None, None

        return method, path, version
             
    def prepare_headers(self, request):
        """Tách phần header trong request thành dictionary."""
        """ 
        Example:
        req = "
        GET /index.html HTTP/1.1\r\n
        Host: localhost\r\n
        User-Agent: curl/7.64.1\r\n\r\n"
        returns {
            'host': 'localhost',
            'user-agent': 'curl/7.64.1'
        }
        """
        lines = request.split('\r\n')
        #Tách request thành các dòng
        headers = {}
        for line in lines[1:]:#Bắt đầu từ dòng thứ 2 bỏ qua request line
            if ': ' in line:
                key, val = line.split(': ', 1)
                headers[key.lower()] = val
        return headers

    def prepare(self, request, routes=None):
        """Prepares the entire request with the given parameters."""
        """ 
        Phân tích toàn bộ request HTTP raw text, gồm:
            +request line
            +headers
            +body
            +cookies
            và gắn route handler nếu có.
        Example:
        raw_request = (
            "POST /login HTTP/1.1\r\n"
            "Host: example.com\r\n"
            "Cookie: sessionid=abc123; theme=dark\r\n"
            "Content-Type: application/x-www-form-urlencoded\r\n"
            "\r\n"
            "username=admin&password=1234"
        )
        req = Request()
        req.prepare(raw_request, routes={('POST', '/login'): login_handler})
        returns Request object with:
            method = 'POST'
            path = '/login'
            version = 'HTTP/1.1'
            headers = {
                'host': 'example.com',
                'cookie': 'sessionid=abc123; theme=dark',
                'content-type': 'application/x-www-form-urlencoded'
            }
            body = 'username=admin&password=1234'
            cookies = {
                'sessionid': 'abc123',
                'theme': 'dark'
            }
            hook = login_handler
        """
    

        # Tách request line:
        self.method, self.path, self.version = self.extract_request_line(request)
        print("[Request] {} path {} version {}".format(self.method, self.path, self.version))

        #
        # @bksysnet Preapring the webapp hook with WeApRous instance
        # The default behaviour with HTTP server is empty routed
        #
        # TODO manage the webapp hook in this mounting point
        #
        
        # Xử lý routes nếu có
        if not routes == {}:
            self.routes = routes
            self.hook = routes.get((self.method, self.path))
            #
            # self.hook manipulation goes here
            # ...
            #
        # Tách headers
        self.headers = self.prepare_headers(request)
        # Tách body nếu có
        parts = request.split('\r\n\r\n', 1)
        if len(parts) > 1:
            self.body = parts[1]
        else:
            self.body = ''

        # Phân tích cookies nếu có
        cookie_header = self.headers.get('cookie', '')
        cookies = {}
        if cookie_header:
            for pair in cookie_header.split(';'):
                if '=' in pair:
                    k, v = pair.strip().split('=', 1)
                    cookies[k] = v
        self.cookies = cookies

        return

    def prepare_body(self, data, files, json=None):
        # Store provided body data and update Content-Length
        self.body = data
        self.prepare_content_length(self.body)
        # TODO prepare the request authentication
        # self.auth = ...
        return


    def prepare_content_length(self, body):
        try:
            length = len(body) if body is not None else 0
        except Exception:
            length = 0
        self.headers["Content-Length"] = str(length)
        # TODO prepare the request authentication
        # self.auth = ...
        return


    def prepare_auth(self, auth, url=""):
        #
        # TODO prepare the request authentication
        #
	# self.auth = ...
        self.auth = get_auth_from_url(url) if url else auth
        return self.auth

    def prepare_cookies(self, cookies):
            self.headers["Cookie"] = cookies
