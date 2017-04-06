#!/usr/bin/env python3

import argparse
from binascii import unhexlify
import socket
import signal
import struct
import sys

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

#TODO Remove
ORIGIN_SERVER = ("ec2-54-166-234-74.compute-1.amazonaws.com", 8080)

# ! = Network (big-endian)
# <2,6> = <2,6> of the next type (e.g unsigned shorts)
# H = unsigned short
BODY_FORMAT = struct.Struct("!2H")
HEADER_STRUCTURE = struct.Struct("!6H")

class DNSServer:
    def __init__(self, name, port, servers=DEFAULT_SERVERS):
        self.name = name
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print("Binding to (\"{}\", {})".format('', port))
        self.sock.bind(('', port))
        # Client connections, which are tuples of (<socket>, <address(str)>)
        self.clients = []

    def listen(self):
        """Listens for and responds to clients forever, in a loop"""
        server = socket.getaddrinfo(ORIGIN_SERVER[0], ORIGIN_SERVER[1])[0][-1][0]
        while True:
            try:
                #self.sock.settimeout(None)
                data, address = self.sock.recvfrom(2048)
                query = DNSQuery(data)
                print("Got data from {}".format(address))
                # TODO Don't give the origin server as a place to go
                query.domain = server
                packet = query.respond(server, self.name)
                self.sock.sendto(packet, address)
                print("Packet sent w/ ip {}".format(server))
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
        self.domain = ''

        head = (data[2] >> 3) & 15
        if head == 0:
            # Header length = 12 bytes
            ini = 12
            length = data[ini]
            while length != 0:
                self.domain += data[ini + 1: ini + length + 1].decode() + '.'
                ini += length + 1
                length = data[ini]

    def respond(self, ip, name):
        packet=bytes()
        if self.domain:
            id = self.data[:2]
            domain_name = b"\x10" + (
                name.encode().replace(b'.', b'\x03') +
                b'\x00\x00\x01' +
                b'\x00\x01')
            return id + unhexlify('81800001000100000001') + domain_name + (
                unhexlify('c00c00010001000000a60004') + unhexlify("acd90b2e0000290200000000000000")# + ip.encode()
            )
            return example_google
            packet += self.data[:2] + b"\x81\x80"
            # Q&A Counts
            packet += self.data[4:6] + self.data[4:6] + b'\x00\x00\x00\x00'
            # Domain question
            packet += self.data[12:]
            #print("domain question: {}".format(self.data[12:]))

            # TODO Everything until next todo is new
            print("domain {}".format(self.domain))
            packet += self.domain.encode()
            # A + IN fields
            packet += b'\x00\x01' * 2
            packet += ip.encode()

            return packet
            # TODO Everything after this is bad, ignore
            # Pointer to domain name
            packet += b'\xc0\x0c'
            # Response type, ttl and resource data length
            packet += b'\x00\x01\x00\x01\x00\x00\x00\x3c\x00\x04'
            packet += ip.encode()
        return packet

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
