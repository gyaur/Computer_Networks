import socket
import struct
import select
import sys
import random


def get_answer(sign, val, rand):
    if sign == "<":
        return "I" if rand < val else "N"
    if sign == ">":
        return "I" if rand > val else "N"
    if sign == "=":
        return "Y" if val == rand else "K"


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((sys.argv[1], int(sys.argv[2])))
server.listen()
rand = random.randrange(1, 101)
connections = []
inp = [server]

print(f"Starting with {rand}")

done = False

while True:
    readable, _, _ = select.select(inp, [], [])
    for s in readable:
        if s is server:
            conn, addr = server.accept()
            inp.append(conn)
            connections.append(conn)
            print(addr)
        else:
            try:
                data = s.recv(4096)
            except:
                continue
            if data:
                if not done:
                    sign, val = struct.unpack("si", data)
                    sign = sign.decode("utf8")
                    ans = get_answer(sign, val, rand)
                    answer = struct.pack("si", bytes(ans, "utf8"), 0)
                    if ans == "Y":
                        done = True
                        for connection in connections:
                            if connection is not s:
                                connection.sendall(
                                    struct.pack("si", bytes("K", "utf8"), 0))
                    s.sendall(answer)
                else:
                    s.sendall(struct.pack("si", bytes("V", "utf8"), 0))
            else:
                s.close()
                inp.remove(s)

server.close()
