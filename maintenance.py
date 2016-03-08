#!/usr/bin/env python

import sys
import BaseHTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler


if sys.argv[1:]:
    port = int(sys.argv[1])
else:
    port = 8080

HandlerClass = SimpleHTTPRequestHandler
ServerClass = BaseHTTPServer.HTTPServer
Protocol = "HTTP/1.0"

server_address = ('', port)

HandlerClass.protocol_version = Protocol
httpd = ServerClass(server_address, HandlerClass)
sa = httpd.socket.getsockname()

print('Serving Maintenance HTTP server on %s:%s' % (sa[0], sa[1]))

try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print('Shutting down HTTP server')
    httpd.socket.close()
