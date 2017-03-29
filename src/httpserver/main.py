#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer

class HTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)

        self.send_header('Content-type', 'text/html')
        self.end_headers()

        message = "Hello world"
        self.wfile.write(bytes(message, 'utf-8'))
        return

print("starting the server yo")

server_address = ("127.0.0.1", 8081)

httpd = HTTPServer(server_address, HTTPHandler)
print('running this shit')
httpd.serve_forever() #FOREVER FOREVER FOREVER
