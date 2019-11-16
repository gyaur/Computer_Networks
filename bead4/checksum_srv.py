import socket
import sys
import hashlib
import select
import time

ip, port = sys.argv[1:]

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ip, int(port)))
server.listen()
store = {}
inp = [server]
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
                if len(temp) == 5 and temp[0] == "BE":
                    op, file_id, validity_time, _, chsum = data.decode().split(
                        "|")
                    store[file_id] = {
                        "chsum": chsum,
                        "valid_until": time.time() + float(validity_time)
                    }
                    s.sendall("OK".encode())
                elif len(temp) == 2 and temp[0] == "KI":
                    op, file_id = data.decode().split("|")
                    if file_id in store.keys(
                    ) and store[file_id]["valid_until"] > time.time():
                        to_send = store[file_id]
                        s.sendall(
                            f"{len(to_send['chsum'])}|{to_send['chsum']}".
                            encode())
                    else:
                        s.sendall("0|".encode())

            else:
                s.close()
                inp.remove(s)
server.close()
