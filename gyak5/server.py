import socket
import struct
import select
import sys
import random

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 12345))
server.listen()
connections = []
inp = [server]

while True:
    readable, _, _ = select.select(inp, [], [])
    for s in readable:
        if s is server:
            conn, addr = server.accept()
            inp.append(conn)
            connections.append(conn)
            print(addr)
        else:
            try:
                data = s.recv(4096)
            except:
                continue
            if data:
                for connection in connections:
                    if connection is not s:
                        connection.sendall(data)
            else:
                s.close()
                inp.remove(s)

server.close()
