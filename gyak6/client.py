import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.sendto(sys.argv[1].encode(), ("localhost", 12345))
print(sock.recvfrom(4096)[0].decode())
sock.close()