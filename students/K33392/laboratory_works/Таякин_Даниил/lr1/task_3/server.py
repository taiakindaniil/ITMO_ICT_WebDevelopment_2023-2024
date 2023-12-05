import socket

def create_http_response(body: str) -> bytes:
  header = f"HTTP/1.2 200 OK\nContent-Type: text/html; charset=utf-8\nContent-Length: {len(body)}"
  request = f"{header}\n\n{body}"
  return request.encode()


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 3001))
s.listen(1)

conn, addr = s.accept()
http_data = create_http_response(open("./index.html").read())
conn.sendall(http_data)
conn.close()