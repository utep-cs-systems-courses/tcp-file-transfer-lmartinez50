# This program use a TCP connection to send files through a Server
#
# Author Lorenzo Martinez
# Version 1.0
# Creation Date: 10/01/2020
# Due date: 10/06/2020
# Lab 2
# CS 4375 Theory of Operating Systems
# Instructor PhD Eric Freudenthal
# Rev. 1 10/01/2020 Initial approach
# Rev. 2 10/02/2020 Adding functionality
# Rev. 3 10/06/2020 Adding comments and messages

import os
import re
import socket
import sys
from stat import *

DIRPATH = "./lib"
sys.path.append(DIRPATH)  # for params
import params

PATH_FILES = "SendFiles/"
CONFIRM_MSG = "File %s received by the server"
REJECT_MSG = "File %s could not be received by the server. Try again"


def client():
    switchesVarDefaults = (
        (('-s', '--server'), 'server', "127.0.0.1:50001"),
        (('-d', '--debug'), "debug", False),  # boolean (set if present)
        (('-?', '--usage'), "usage", False),  # boolean (set if present)
    )

    paramMap = params.parseParams(switchesVarDefaults)

    server, usage, debug = paramMap["server"], paramMap["usage"], paramMap["debug"]

    if usage:
        params.usage()

    try:
        serverHost, serverPort = re.split(":", server)
        serverPort = int(serverPort)
    except:
        print("Can't parse server:port from '%s'" % server)
        sys.exit(1)

    addr_port = (serverHost, serverPort)

    # create socket object
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.connect(addr_port)

    while True:
        filename = input("> ")
        filename.strip()

        if filename == "exit":
            sys.exit(0)
        else:
            if not filename:
                continue
            elif os.path.exists(PATH_FILES + filename):
                # send file name
                listen_socket.sendall(filename.encode())
                file_content = open(PATH_FILES + filename, "rb")

                # send file size
                listen_socket.sendall(str(os.stat(PATH_FILES + filename).st_size).encode())

                # send file content
                while True:
                    data = file_content.read(1024)
                    listen_socket.sendall(data)
                    if not data:
                        break
                file_content.close()
            else:
                print("File %s not found" % filename)


if __name__ == "__main__":
    client()
