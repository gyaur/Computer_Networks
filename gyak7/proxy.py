import socket

tcp_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
udp_sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

udp_sock.bind(("localhost",12345))
tcp_sock.bind(("localhost",11111))

while True:
    cli_mes,cli_addr = udp_sock.recvfrom(1024)
    tcp_sock.send(cli_mes)
    serv_mes = tcp_sock.recv(1024)
    udp_sock.sendto(serv_mes,cli_addr)
