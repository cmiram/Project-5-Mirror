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
import pickle


CACHE_DIR = "./cache"
MAX_TEMP_CACHE_SIZE = 0.85 * (10 * 1000 * 1000) #Make cache at max 85% of free space to allow for overhead

class HTTPServer(object):
    def __init__(self, port, origin):
        self.port = port
        self.origin = origin
        self.runtime_cache = {}
        self._build_cache()


    def _build_cache(self):
        self.cache = {}
        for f in os.listdir(CACHE_DIR):
            self.cache.update({"/wiki/" + f.split("-")[0].strip(): CACHE_DIR + "/" + f})

    def fetch_from_cache(self):
        path = self.cache.get(self.path, None)
        if path == None
            return self.runtime_cache.get(self.path)

        with open(path, "rb") as f:
            return f.read()


    def runtime_cache_size(self):
        return sys.getsizeof(pickle.dumps(self.runtime_cache))
        
    def add_to_runtime_cache(self, path, res):
        self.runtime_cache.update({path: res})
        while runtime_cache_size() > MAX_TEMP_CACHE_SIZE
            self.runtime_cache.pop()


    def parse_request(self, req):
        req_line = req.splitlines()[0]
        req_line = req_line.rstrip(b'\r\n')
        (self.request_method, self.path, self.request_version) = req_line.split()

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
                if self.path not in self.cache and self.path not in self.runtime_cache:
                    try:
                        request = 'http://' + self.origin + ':8080' + self.path.decode()
                        res = urlopen(request)
                        self.add_to_runtime_cache(self.path, res.read())
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
                    content = self.fetch_from_cache()
                    client_conn.send(b"""HTTP/1.0 200 OK
                    Content-Type: text/html

                    """  + content)
                    client_conn.close()
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

    server = HTTPServer(port, origin);
    server.serve_forever()

if __name__ == "__main__":
    main()
