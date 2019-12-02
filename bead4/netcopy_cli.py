import socket
import sys
import hashlib

srv_ip, srv_port, chsum_ip, chsum_port, file_id, file_path = sys.argv[1:]

chsum_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
nc_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
chsum_sock.connect((chsum_ip, int(chsum_port)))
chsum = hashlib.md5()
with open(file_path, "rb") as f:
    data = f.read()
    chsum.update(data)
    chsum = chsum.hexdigest()

    chsum_sock.sendall(f"BE|{file_id}|60|{len(chsum)}|{chsum}".encode())
    chsum_sock.recv(4096)
    chsum_sock.close()

with open(file_path, "rb") as f:
    nc_sock.connect((srv_ip, int(srv_port)))
    nc_sock.sendall(f.read())
    nc_sock.close()
