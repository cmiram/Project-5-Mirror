#!/usr/bin/env python3

import requests
import argparse
from http.server import BaseHTTPRequestHandler, HTTPServer

class HTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # TODO make this not magically set
        global origin
        r = requests.get('http://' + origin + ":8080" + self.path)
        self.send_response(200)

        self.send_header('Content-type', 'text/html')
        self.end_headers()

        self.wfile.write(r.content)
        return




def main():
    global origin
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', metavar="port", type=int)
    parser.add_argument('-o', metavar='origin', type=str)
    args = parser.parse_args()
    print(args)
    port = args.p
    origin = args.o
    print("starting the server yo, port {}", port)

    server_address = ("127.0.0.1", port)

    httpd = HTTPServer(server_address, HTTPHandler)
    httpd.serve_forever() #FOREVER FOREVER FOREVER

if __name__ == "__main__":
    main()
