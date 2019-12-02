import sys
import socket
ip, port = "localhost", 12345
ip, port = sys.argv[1:]
address = (ip, int(port))

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(address)
power = True

try:
    while True:
        data, addr = sock.recvfrom(1024)
        data = data.decode()
        if not power and data != "Power":
            sock.sendto(f"Powered off".encode(), addr)
        elif data == "Power":
            power = not power
            sock.sendto(f"Powered {'on' if power else 'off'}".encode(), addr)
        elif data in ("Espresso", "Capucino"):
            sock.sendto(f"Enjoy your {data}".encode(), addr)
        else:
            sock.sendto(f"I dont know what is: {data}".encode(), addr)

except:
    sock.close()