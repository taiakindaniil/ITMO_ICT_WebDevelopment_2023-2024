import socket
import json
from collections import defaultdict
from dataclasses import dataclass
from http import HTTPStatus
from urllib.parse import urlparse, parse_qs

DB = defaultdict(list)


@dataclass
class HTTPRequest:
  method: str
  url: str
  protocol: str
  headers: dict[str, str]
  body: bytes


@dataclass
class HTTPResponse:
  status: int
  headers: dict[str, str]
  body: bytes
  protocol: str = "HTTP/1.2"

  def __bytes__(self):
    headers_str = "\n".join(f"{key}: {val}" for key, val in self.headers.items())
    return f"{self.protocol} {self.status} {HTTPStatus(self.status).phrase}\n{headers_str}\n\n".encode() + self.body


class MyHTTPServer:

  def __init__(self, host: str, port: int) -> None:
    self.host = host
    self.port = port
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  
  def serve_forever(self):
    self.socket.bind((self.host, self.port))
    self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self.socket.listen()
    while True:
      conn, addr = self.socket.accept()
      self.serve_client(conn)

  def serve_client(self, conn: socket.socket):
    req = self.parse_request(conn)
    resp = self.handle_request(req)
    self.send_response(conn, resp)

    if conn:
      conn.close()

  def parse_request(self, conn: socket.socket) -> HTTPRequest:
    lines = conn.recv(1024*10).splitlines()

    # parse first line
    try:
      method, url, protocol = lines[0].decode().strip().split()
    except IndexError:
      raise Exception("First line is incorrect")

    headers, body_start_index = self.parse_headers(lines)
    body = b"".join(lines[body_start_index + 2:])

    return HTTPRequest(method, url, protocol, headers, body)

  def parse_headers(self, lines) -> dict[str, str]:
    headers: dict[str, str] = {}
    index = 1
    req_generator = ( (n, i.decode()) for n, i in enumerate(lines[1:], 1) )
    while (data := next(req_generator, None)) is not None and data[1].strip() != "":
      index, header = data
      try:
        key, val = header.split(":", 1)
        headers[key.lower()] = val.strip()
      except ValueError:
        raise Exception("Headers are incorrect")
    return headers, index

  def handle_request(self, req: HTTPRequest) -> HTTPResponse:
    parsed_url = urlparse(req.url)
    query = parse_qs(parsed_url.query)

    print(req)

    if req.method == "GET" and parsed_url.path == "/scores":
      if "subject" not in query:
        return HTTPResponse(
          status=400,
          headers={"Content-Type": "application/json"},
          body=json.dumps({"desc": "you need to specify subject param"}).encode()
        )

      return HTTPResponse(
        status=200,
        headers={"Content-Type": "text/html; charset=utf-8"},
        body=f"""
        <!DOCTYPE html><html><body>
          <table>
            <tr><th>{query['subject'][0]}</th></tr>
            <tr>
              <td>{"</td><td>".join(DB[query['subject'][0]])}</td>
            </tr>
          </table>
        </body></html>""".encode()
      )
    elif req.method == "POST" and parsed_url.path == "/subject":
      if "name" not in query:
        return HTTPResponse(
          status=400,
          headers={"Content-Type": "application/json"},
          body=json.dumps({"desc": "you need to specify name param"}).encode()
        )
      if "score" not in query:
        return HTTPResponse(
          status=400,
          headers={"Content-Type": "application/json"},
          body=json.dumps({"desc": "you need to specify score param"}).encode()
        )
      DB[query["name"][0]].append(query["score"][0])
      return HTTPResponse(status=200, headers={}, body=b"")
    return HTTPResponse(status=400, headers={}, body=b"")

  def send_response(self, conn: socket.socket, resp: HTTPResponse):
    conn.sendall(bytes(resp))


if __name__ == "__main__":
  server = MyHTTPServer("localhost", 3004)
  try:
    server.serve_forever()
  except KeyboardInterrupt:
    pass