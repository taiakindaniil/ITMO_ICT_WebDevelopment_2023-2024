import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('', 3001))

msg = s.recv(1024).decode()
print(msg)

data = input().encode()
s.send(data)
print(s.recv(1024).decode())