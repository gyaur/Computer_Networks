import sys
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_addr = ("localhost", 12346)


def handshake():
    sock.sendto("SYN".encode(), server_addr)
    data, _ = sock.recvfrom(1024)
    if data.decode() != "SYN-ACK":
        print(data.decode())
        return False
    sock.sendto("ACK".encode(), server_addr)
    return True


things = ["Espresso", "Power", "Tea", "Power", "Tea", "Capucino"]
try:
    for i in things:
        if (handshake()):
            print("Hand shook")
            sock.sendto(i.encode(), server_addr)
            print(sock.recvfrom(1024)[0])
        else:
            print(sock.recvfrom(1024)[0].decode())

except:
    sock.close()