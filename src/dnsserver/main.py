#!/usr/bin/env python

from __future__ import unicode_literals

import argparse
import socket
import signal
import struct
import sys

from binascii import unhexlify
from random import choice

DEFAULT_SERVERS=[
    'ec2-52-90-80-45.compute-1.amazonaws.com',
    'ec2-54-183-23-203.us-west-1.compute.amazonaws.com',
    'ec2-54-70-111-57.us-west-2.compute.amazonaws.com',
    'ec2-52-215-87-82.eu-west-1.compute.amazonaws.com',
    'ec2-52-28-249-79.eu-central-1.compute.amazonaws.com',
    'ec2-54-169-10-54.ap-southeast-1.compute.amazonaws.com',
    'ec2-52-62-198-57.ap-southeast-2.compute.amazonaws.com',
    'ec2-52-192-64-163.ap-northeast-1.compute.amazonaws.com',
    'ec2-54-233-152-60.sa-east-1.compute.amazonaws.com',
]

class DNSServer:
    def __init__(self, name, port, servers=DEFAULT_SERVERS):
        self.name = name
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('', port))
        # Client connections, which are tuples of (<socket>, <address(str)>)
        self.clients = []

    def listen(self):
        """Listens for and responds to clients forever, in a loop"""
        while True:
            try:
                #self.sock.settimeout(None)
                data, address = self.sock.recvfrom(2048)
                query = DNSQuery(data)
                # TODO Don't give the origin server as a place to go
                packet = query.respond(socket.getaddrinfo(choice(DEFAULT_SERVERS),
                                                          8080)[0][-1][0],
                                       self.name)
                self.sock.sendto(packet, address)
                # TODO Lookup address in hashmap, send them to that one.

            except (socket.timeout, socket.error):
                try:
                    client.close()
                except (socket.error, UnboundLocalError):
                    pass


    def close(self):
        self.sock.close()

class DNSQuery:
    def __init__(self, data):
        self.data = data

    def respond(self, ip, name):
        id = self.data[:2]
        domain_name = b"\x09" + (
            name.encode().replace(b'.', b'\x07', 1).replace(b'.', b'\x03') +
            b'\x00\x00\x01' +
            b'\x00\x01')
        return id + (
            # Magic header / question + domain name
            unhexlify('81800001000100000001') + domain_name +
            # Magic answer pre-cursor
            unhexlify('c00c00010001000000a60004') + socket.inet_aton(ip))

def main():
    global origin
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', metavar="port", type=int)
    parser.add_argument('-n', metavar='name', type=str)
    args = parser.parse_args()
    port = args.p
    name = args.n
    global server
    server = DNSServer(name, port)
    def sigint_handler(signal, frame):
        global server
        server.close()
        sys.exit(0)
    signal.signal(signal.SIGINT, sigint_handler)
    try:
        server.listen()
    except Exception as e:
        server.close()
        raise

if __name__ == "__main__":
    main()
