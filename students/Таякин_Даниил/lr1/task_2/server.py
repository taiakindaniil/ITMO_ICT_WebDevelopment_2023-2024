import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 3001))
s.listen(1)

conn, addr = s.accept()
conn.send(b"Enter a b sides of right triangle:")

data = conn.recv(1024)
a, b = list(map(int, data.decode().split()))
hypotenuse = (a**2 + b**2) ** 0.5

conn.sendall(str(hypotenuse).encode())
conn.close()