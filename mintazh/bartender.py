import socket

address = ("localhost", 12346)

servers = [("localhost", 12345), ("localhost", 12347)]

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(address)


def handshake():
    data, addr = sock.recvfrom(1024)
    if data.decode() != "SYN":
        sock.sendto("No hanshake".encode(), addr)
        return False
    sock.sendto("SYN-ACK".encode(), addr)
    data, addr = sock.recvfrom(1024)
    if data.decode() != "ACK":
        sock.sendto("No hanshake".encode(), addr)
        return False
    return True


try:
    while True:
        for server in servers:
            if handshake():
                data, user_addr = sock.recvfrom(1024)
                data = data.decode()
                if data == "Tea":
                    sock.sendto("Enjoy your Tea".encode(), user_addr)
                else:
                    sock.sendto(data.encode(), server)
                    data, _ = sock.recvfrom(1024)
                    sock.sendto(data, user_addr)

except:
    sock.close()
