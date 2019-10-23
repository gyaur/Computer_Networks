import socket
import sys
import select

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect(("localhost", 12345))

while True:
    readable, _, _ = select.select([sock, sys.stdin], [], [])
    for s in readable:
        if s is sock:
            print(sock.recv(1024).decode())
        else:
            sock.send(sys.stdin.readline().encode())