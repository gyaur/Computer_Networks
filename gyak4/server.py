import socket
import pickle
import select

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 8082))
server.listen(1)
inputs = [server]
try:
    while True:
        readable, _, _ = select.select(inputs, [], [])
        for s in readable:
            if s is server:
                conn, addr = server.accept()
                inputs.append(conn)
            else:
                data = s.recv(4096)
                if data:
                    data = pickle.loads(data)
                    s.sendall(
                        pickle.dumps(eval(f"{data[0]}{data[2]}{data[1]}")))
                else:
                    s.close()
                    inputs.remove(s)
finally:
    server.close()
