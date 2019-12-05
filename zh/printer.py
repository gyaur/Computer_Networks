import socket
import sys
import select

server_address = ("localhost", 55556)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(server_address)
server.listen(2)

auth_server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
auth_server_addr = ("localhost", 12346)
sessions = {}
inp = [server]

try:
    while True:
        readable, _, _ = select.select(inp, [], [])
        for s in readable:
            if s is server:
                conn, addr = server.accept()
                inp.append(conn)
            else:
                data = s.recv(4096)
                if data:
                    temp = data.decode().split("|")
                    if temp[0] == "Auth":
                        com, uname, sess_id = temp
                        auth_server_sock.sendto(
                            f"Validate|{uname}|{sess_id}".encode(),
                            auth_server_addr)
                        ans, _ = auth_server_sock.recvfrom(4096)
                        if ans.decode() == "True":
                            sessions[s] = uname
                            s.sendall("OK".encode())
                        else:
                            s.sendall("Invalid sessionid".encode())
                    elif temp[0] == "Print":
                        com, file = temp
                        if s in sessions.keys():
                            s.sendall("Printed".encode())
                        else:
                            s.sendall("Validate yourself".encode())

                    elif temp[0] == "Disconnect":
                        if s in sessions.keys():
                            inp.remove(s)
                            sessions.pop(s, None)
                            if s in sessions.keys():
                                auth_server_sock.sendto(
                                    f"Logout|{sessions[s]}".encode(),
                                    auth_server_addr)
                                auth_server_sock.recvfrom(1024)
                            s.sendall("Disconnected yourself".encode())
                            s.close()
                        else:
                            s.sendall("Validate yourself".encode())
                else:
                    s.close()
                    inp.remove(s)
                    if s in sessions.keys():
                        auth_server_sock.sendto(
                            f"Logout|{sessions[s]}".encode(), auth_server_addr)
                        auth_server_sock.recvfrom(1024)
                    sessions.pop(s, None)
finally:
    server.close()
    auth_server_sock.close()
