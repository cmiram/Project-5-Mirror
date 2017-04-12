#!/usr/bin/env python

from __future__ import unicode_literals
try:
    from urllib import request
    from urllib.request import urlopen
except ImportError:
    # Python 2
    from urllib2 import Request as request
    from urllib import urlopen

import argparse
import json
import math
import socket
import signal
import struct
import sys

from binascii import unhexlify

DEFAULT_SERVERS = [
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

PUBLIC_IP = json.loads(urlopen("https://api.ipify.org?format=json").read())["ip"]

class DNSServer:
    def __init__(self, name, port, servers=DEFAULT_SERVERS):
        self.name = name
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('', port))
        # Client connections, which are dicts of {ip(str): [List of latencies(float)]}
        self.clients = {}
        # Coordinates of the servers, used to calculate a better thing than "random"
        # [(lat(float), long(float))]
        self.cords = []
        for server in DEFAULT_SERVERS:
            self.cords.append(get_cords(server))

    def listen(self):
        """Listens for and responds to clients forever, in a loop"""
        while True:
            try:
                data, address = self.sock.recvfrom(2048)
                ip = address[0]
                query = DNSQuery(data)
                if ip not in self.clients:
                    # New client, send to a random one.
                    server = self.closest_server(ip)
                    self.clients.update({ip: [-1 for _ in DEFAULT_SERVERS]})
                    self.clients[ip][DEFAULT_SERVERS.index(server)] = 0
                else:
                    server_latencies = self.clients[ip]
                    lowest = None
                    lowest_index = 0
                    for index, latency in enumerate(server_latencies):
                        if not lowest or latency > lowest:
                            lowest = latency
                            lowest_index = index
                    server = DEFAULT_SERVERS[lowest_index]
                packet = query.respond(socket.getaddrinfo(server,
                                                            8080)[0][-1][0],
                                    self.name)
                self.sock.sendto(packet, address)


            except (socket.timeout, socket.error):
                try:
                    client.close()
                except (socket.error, UnboundLocalError):
                    pass

    def closest_server(self, hostname):
        """Finds the closest default server for the given hostname.
        It does this by looking up the lat/long and doing maths"""
        host_cords = get_cords(hostname)
        if host_cords[0] == 0 and host_cords[1] == 0:
            host_cords = get_cords(PUBLIC_IP)
        earth_radius = 6371 # Radius in kilometers
        min_index = 0
        min = None
        for (index, server_cords) in enumerate(self.cords):
            lat = math.radians(server_cords[0] - host_cords[0])
            long = math.radians(server_cords[1] - host_cords[1])
            sin_lat = math.sin(lat / 2)
            sin_long = math.sin(long / 2)
            a = (math.pow(sin_lat, 2) + math.pow(sin_long, 2)
                 * math.cos(math.radians(host_cords[0]))
                 * math.cos(math.radians(server_cords[0])))
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
            dist = earth_radius * c
            if not min or min > dist:
                min = dist
                min_index = index
        return DEFAULT_SERVERS[index]

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
            unhexlify('c00c000100010000001e0004') + socket.inet_aton(ip))

def get_cords(hostname):
    """Returns a tuple of lat/long. Used for initial redirect calculations."""
    ip = socket.getaddrinfo(hostname, 8080)[0][-1][0]
    response = urlopen("http://freegeoip.net/json/" + ip)
    data = json.loads(response.read())
    return (data["latitude"], data["longitude"])

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
