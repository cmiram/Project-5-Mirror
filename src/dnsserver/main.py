#!/usr/bin/env python

import argparse
import socket
import signal
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

class DNSServer:
    def __init__(self, name, port, servers=DEFAULT_SERVERS):
        self.name = name
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((name, port))
        # Client connections, which are tuples of (<socket>, <address(str)>)
        self.clients = []

    def listen(self):
        """Listens for and responds to clients forever, in a loop"""
        while True:
            try:
                self.sock.settimeout(None)
                client, address = self.sock.recvfrom(2048)
                print("Got client {}, from {}".format(client, address))
                # TODO Lookup address in hashmap, send them to that one.
                data = client.recv(2048)
                print("Got back {}".format(data))

            except (socket.timeout, socket.error):
                try:
                    client.close()
                except (socket.error, UnboundLocalError):
                    pass

    def close(self):
        #self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()


def main():
    global origin
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', metavar="port", type=int)
    parser.add_argument('-n', metavar='name', type=str)
    args = parser.parse_args()
    port = args.p
    name = args.n
    print("starting the server yo, port {}, name {}".format( port, name))

    global server
    server = DNSServer("", port)
    def sigint_handler(signal, frame):
        global server
        server.close()
        sys.exit(0)
    signal.signal(signal.SIGINT, sigint_handler)
    try:
        server.listen()
    except Exception as e:
        print("error: {}".format(e))
        server.close()

if __name__ == "__main__":
    main()
