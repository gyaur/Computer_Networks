import socket
import sys
import hashlib

srv_ip, srv_port, chsum_ip, chsum_port, file_id, file_path = sys.argv[1:]

rec_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
rec_sock.bind((srv_ip, int(srv_port)))
rec_sock.listen()
conn, addr = rec_sock.accept()
with open(file_path, "wb") as f:
    data = conn.recv(4096)
    while data:
        f.write(data)
        data = conn.recv(4096)

chsum_file = hashlib.md5()
with open(file_path, "rb") as f:
    while True:
        data = f.read(65536)
        if not data:
            break
        chsum_file.update(data)
    chsum_file = chsum_file.hexdigest()

rec_sock.close()

chsum_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
chsum_sock.connect((chsum_ip, int(chsum_port)))
chsum_sock.sendall(f"KI|{file_id}".encode())
_, chsum = chsum_sock.recv(4096).decode().split("|")
# print(chsum)
chsum_sock.close()

print("CSUM OK" if chsum_file == chsum else "CSUM CORRUPTED")
