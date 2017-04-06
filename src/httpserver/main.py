#!/usr/bin/env python3

import requests
import argparse
import socket
import urllib2
import os
import errno

class HTTPServer(object):
	def __init__(port, origin, cache):
		self.port = port
		self.origin = origin
		self.cache = cache
	
	def parse_request(self, req):
		req_line = req.splitlines()[0]
		req_line = req_line.rstrip('\r\n')
		(self.request_method, self.path, self.request_version) = req_line.split()
		
	def send_res(status):
		
		
	def send_header(content, type):
		
		
	def end_header:
		
		
	def download(self, path, response):
		fname = os.pardir + path
		dest = os.path.dirname(fname)
		is_done = False if not os.path.exists(dest)
			os.makedirs(dest)
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
		socket_listen.bind(('', PORT))
		socket_listen.listen(1)
		
		while True:
			client_conn, client_addr = socket_listen.accept()
			requet = client_conn.recv(1024)
			self.parse_request(request);
			if self.path not in self.cache:
				try:
					request = 'http://' + self.origin + ':' + self.port + self.path
					res = urllib2.urlopen(request)
					return
				except urllib2.HTTPError as err:
					self.send_error(err.code, err.reason)
					return
				except urllib2.URLError as err:
					self.send_error(err.reason)
					return
			else:
				self.download(self.path, res)
			
			with open(os.pardir + self.path) as html:
				self.send_res(200)
				self.send_header('Content-type', 'text/plain')
				self.end_header()
				self.wfile.write(html.read())
			
			self.cache.append(self.path) #add new info to cache
			
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
	cache = []
	def server:
		HTTPServer(port, origin, cache);
	server.serve_forever()

if __name__ == "__main__":
    main()
