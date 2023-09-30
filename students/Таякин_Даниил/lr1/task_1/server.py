import socket

# creating socket obj, where
# AF_INET - IPv4 family
# SOCK_DGRAM - UDP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

s.bind(('', 3001))

# receive data (1024 bytes) and ip address from a client
data, client_addr = s.recvfrom(1024)
print(data.decode())

# send a response to the client
s.sendto(b"Hello, Client!", client_addr)