import sys
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
auth_server_addr = ("localhost", 12346)

printer_addr = ("localhost", 55556)
tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_sock.connect(printer_addr)
try:
    while True:
        inp = input("command: ")
        if inp.split("|")[0] in ["Login", "Logout", "Validate"]:
            sock.sendto(inp.encode(), auth_server_addr)
            print(sock.recvfrom(1024)[0])
        elif inp.split("|")[0] in ["Auth", "Print", "Disconnect"]:
            tcp_sock.sendall(inp.encode())
            print(tcp_sock.recv(4096).decode())
finally:
    sock.close()
    tcp_sock.close()
