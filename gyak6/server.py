import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("localhost", 12345))
try:
    while True:
        data, address = sock.recvfrom(4096)
        print(data.decode())
        s_data = str(eval(data.decode()))
        sock.sendto(s_data.encode(), address)
finally:
    sock.close()
