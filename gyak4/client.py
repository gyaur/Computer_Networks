import socket
import pickle
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect(("0.0.0.0", 8082))

sock.sendall(pickle.dumps((sys.argv[1], sys.argv[2], sys.argv[3])))
print(pickle.loads(sock.recv(4096)))
