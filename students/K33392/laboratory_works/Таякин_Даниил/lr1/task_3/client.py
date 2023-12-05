import socket


def read_server_data(s: socket.socket, chunk_size=1024) -> bytes:
  result = b""
  while True:
    data = s.recv(chunk_size)
    if not data:
      break
    result += data
  return result


def read_http_body(response: bytes) -> str:
  lines = response.decode().splitlines()
  body_start = next((i for i, line in enumerate(lines) if line == ""), -1)
  if body_start == -1:
    raise ValueError("Invalid HTTP")
  return "\n".join(lines[body_start + 1:])


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('', 3001))

data = read_server_data(s)
body = read_http_body(data)

print(body)