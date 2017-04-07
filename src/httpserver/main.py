#!/usr/bin/env python2

import argparse
import socket
try:
    from urllib.error import HTTPError, URLError
    from urllib import request
    from urllib.request import urlopen
except ImportError:
    # Python 2
    from urllib2 import HTTPError, URLError, Request as request
    from urllib import urlopen
    import urllib2 as urllib
import os
import errno

class HTTPServer(object):
    def __init__(self, port, origin, cache):
        self.port = port
        self.origin = origin
        self.cache = cache

    def parse_request(self, req):
        req_line = req.splitlines()[0]
        req_line = req_line.rstrip(b'\r\n')
        (self.request_method, self.path, self.request_version) = req_line.split()

    def download(self, path, response):
        fname = os.pardir + path
        dest = os.path.dirname(fname)
        is_done = os.makedirs(dest) if os.path.exists(dest) else False
        fd = open(fname, 'w')
        while not is_done:
            try:
                fd.write(response.read())
                is_done = Trueself.cache.append(path)
            except IOError as err:
                if err.errno == errno.EDQuot:
                    to_remove = self.cache.pop(0) #remove first one
                    os.remove(os.pardir + to_remove)
                else:
                    raise err

        fd.close()


    def serve_forever(self):
        socket_listen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_listen.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        socket_listen.bind(('', self.port))
        socket_listen.listen(1)

        while True:
            try:
                client_conn, client_addr = socket_listen.accept()
                request = client_conn.recv(1024)
                self.parse_request(request);
                if self.path not in self.cache:
                    try:
                        request = 'http://' + self.origin + ':' + str(self.port) + self.path.decode()
                        res = urlopen(request)
                        client_conn.send(b"""HTTP/1.0 200 OK
    Content-Type: text/html

    """  + res.read())
                        client_conn.close()
                    except HTTPError as err:
                        raise
                        self.send_error(err.code, err.reason)
                    except URLError as err:
                        raise
                        self.send_error(err.reason)
                else:
                    self.download(self.path, res)
            except Exception as e:
                pass



def main():
    global origin
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', metavar="port", type=int)
    parser.add_argument('-o', metavar='origin', type=str)
    args = parser.parse_args()
    port = args.p
    origin = args.o

    cache = []
    server = HTTPServer(port, origin, cache);
    server.serve_forever()

if __name__ == "__main__":
    main()
