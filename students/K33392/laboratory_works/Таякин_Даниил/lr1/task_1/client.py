import socket

# creating socket obj, where
# AF_INET - IPv4 family
# SOCK_DGRAM - UDP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# send bytes to the server address
s.sendto(b"Hello, Server!", ('', 3001))

# wait for server reply
data = s.recv(1024)
print(data.decode())