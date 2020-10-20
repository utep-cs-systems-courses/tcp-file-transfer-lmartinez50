# This program use a TCP connection to send files through a Server
# using threads
# Author Lorenzo Martinez
# Version 2.0
# Creation Date: 10/15/2020
# Due date: 10/19/2020
# Lab 2
# CS 4375 Theory of Operating Systems
# Instructor PhD Eric Freudenthal
# Rev. 1 10/15/2020 Initial approach
# Rev. 2 10/17/2020 Adding functionality
# Rev. 3 10/19/2020 Adding comments

import os
import re
import socket
import sys

DIRPATH = "./lib"
sys.path.append(DIRPATH)  # for params
import params
from framedSocket import framedSocket

PATH_FILES = "SendFiles/"
CONFIRM_MSG = "File %s received by the server"
REJECT_MSG = "File %s could not be received by the server. Try again"
EMPTY_MSG = "File %s was empty. Try again"


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
        print("can't parse server:port from '%s'" % server)
        sys.exit(1)

    addr_port = (serverHost, serverPort)

    # create socket object
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.connect(addr_port)

    # create encapsulated socket
    encap_socket = framedSocket((listen_socket, addr_port))

    while True:
        filename = input("Enter the file to be sent: ")
        filename.strip()

        if filename == "exit":
            sys.exit(0)
        else:
            if not filename:
                continue
            elif os.path.exists(PATH_FILES + filename):
                # open file and read
                file = open(PATH_FILES + filename, "rb")
                file_content = file.read()

                # verify file is not empty before sending
                if len(file_content) < 1:
                    print(EMPTY_MSG % filename)
                    continue

                # send file contents to server
                encap_socket.send(filename, file_content, debug)

                # check if server received file
                status = encap_socket.get_status()
                status = int(status.decode())

                # successful transfer
                if status:
                    print(CONFIRM_MSG % filename)
                    #sys.exit(0)
                # failed transfer
                else:
                    print(REJECT_MSG % filename)
                    sys.exit(1)

            # file not found
            else:
                print("ERROR: file %s not found. Try again" % filename)


if __name__ == "__main__":
    client()