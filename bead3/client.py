import socket
import sys
import struct
from itertools import filterfalse


def interpret(ans, sign, val, possible_values):
    if sign == ">" and ans == "I":
        return list(filter(lambda x: x > val, possible_values))
    if sign == "<" and ans == "N":
        return list(filterfalse(lambda x: x < val, possible_values))
    if sign == ">" and ans == "N":
        return list(filterfalse(lambda x: x > val, possible_values))
    if sign == "<" and ans == "I":
        return list(filter(lambda x: x < val, possible_values))
    return [val]


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect((sys.argv[1], int(sys.argv[2])))

ans = ""

possible_values = list(range(1, 101))

while ans not in ["K", "V", "Y"]:
    sign = "<" if len(possible_values) != 1 else "="
    val = possible_values[len(possible_values) // 2]
    send = struct.pack("si", bytes(sign, "utf8"), val)
    sock.sendall(send)
    ans, _ = struct.unpack("si", sock.recv(4096))
    ans = ans.decode("utf8")
    print(ans, sign, val)
    possible_values = interpret(ans, sign, val, possible_values)
    print(possible_values)

sock.close()