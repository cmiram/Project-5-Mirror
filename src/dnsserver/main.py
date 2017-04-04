#!/usr/bin/env python3

import requests
import argparse
import socket

def main():
    global origin
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', metavar="port", type=int)
    parser.add_argument('-n', metavar='name', type=str)
    args = parser.parse_args()
    port = args.p
    name = args.n
    print("starting the server yo, port {}, name {}".format( port, name))

    server_address = ("127.0.0.1", port)

    # TODO Setup dns server

if __name__ == "__main__":
    main()
