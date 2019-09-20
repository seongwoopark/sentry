#!/usr/bin/python3.6
from pyftpdlib import servers
from pyftpdlib.handlers import FTPHandler


if __name__ == "__main__":
    server = servers.FTPServer(address_or_socket=("0.0.0.0", 21), handler=FTPHandler)
    server.serve_forever()
