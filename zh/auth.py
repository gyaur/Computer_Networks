import socket

address = ("localhost", 12346)

keys = {"jozsi": "alma", "pista": "korte"}
ids = {}
sess_id = 0
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(address)
try:
    while True:
        data, user_addr = sock.recvfrom(1024)
        data = data.decode()
        temp = data.split("|")
        if temp[0] == "Login":
            com, uname, passw = temp
            if uname in keys.keys() and keys[uname] == passw:
                sock.sendto(f"{sess_id}".encode(), user_addr)
                ids[uname] = sess_id
                sess_id += 1
            else:
                sock.sendto(f"Invalid username or password".encode(),
                            user_addr)
        elif temp[0] == "Logout":
            com, uname = temp
            ids.pop(uname, None)
            print(f"{uname} logged out")
            sock.sendto(f"Logged out".encode(), user_addr)
        elif temp[0] == "Validate":
            com, uname, sess = temp
            if uname in ids.keys() and ids[uname] == int(sess):
                sock.sendto(f"True".encode(), user_addr)
            else:
                sock.sendto(f"False".encode(), user_addr)

        else:
            sock.sendto(data.encode(), server)
            data, _ = sock.recvfrom(1024)
            sock.sendto(data, user_addr)
except:
    sock.close()