# Лабораторная работа #1

## Задание #1

### Описание
Реализовать клиентскую и серверную часть приложения. Клиент отсылает серверу
сообщение «Hello, server». Сообщение должно отразиться на стороне сервера.
Сервер в ответ отсылает клиенту сообщение «Hello, client». Сообщение должно
отобразиться у клиента.

- Обязательно использовать библиотеку `socket`
- Реализовать с помощью протокола UDP

### Решение

**Сервер**

Импортируем библиотеку `socket`. Создаем объект socket и связываем его с нашим хостом и с портом 3001.
```python
import socket

# creating socket obj, where
# AF_INET - IPv4 family
# SOCK_DGRAM - UDP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

s.bind(('', 3001))
```

Получаем данные с максимальным размером 1024 байта и ip-адрес клиента. Затем выводим декодированные данные с utf-8 кодировкой.
```python
# receive data (1024 bytes) and ip address from a client
data, client_addr = s.recvfrom(1024)
print(data.decode())
```

Отправляем клиенту ответ: "Hello, Client!".
```python
# send a response to the client
s.sendto(b"Hello, Client!", client_addr)
```

**Клиент**

Импортируем библиотеку `socket` и создаем объект socket.
```python
import socket

# creating socket obj, where
# AF_INET - IPv4 family
# SOCK_DGRAM - UDP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
```

Отправляем данные на сервер с известным нам портом 3001.
```python
# send bytes to the server address
s.sendto(b"Hello, Server!", ('', 3001))
```

Ждем ответ от сервера и выводим его.
```python
# wait for server reply
data = s.recv(1024)
print(data.decode())
```

***

## Задание #2

### Описание
Реализовать клиентскую и серверную часть приложения. Клиент запрашивает у
сервера выполнение математической операции, параметры, которые вводятся с
клавиатуры. Сервер обрабатывает полученные данные и возвращает результат
клиенту.

Вариант: **Теорема Пифагора**

- Обязательно использовать библиотеку `socket`
- Реализовать с помощью протокола TCP

### Решение

**Сервер**

Создаем сокет с протоколом TCP и привязываем его к данному хосту с портом 3001. С помощью метода `listen` запускаем режим прослушивания для данного сокета с максимальным количеством подключений равному 1.
```python
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 3001))
s.listen(1)
```

Ожидаем поключение к серверу. После того, как клиент подключится, сервер отправит сообщение-подсказку.
```python
conn, addr = s.accept()
conn.send(b"Enter a b sides of right triangle:")
```

Одидаем ответ от клиента, обрабатываем его полученные данные и отправляем ответ с результатом вычисленной гипотенузы.
```python
data = conn.recv(1024)
a, b = list(map(int, data.decode().split()))
hypotenuse = (a**2 + b**2) ** 0.5

conn.sendall(str(hypotenuse).encode())
conn.close()
```

**Клиент**

Подключаемся к TCP серверу. 
```python
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('', 3001))
```

Получаем сообщение-подсказку. 
```python
msg = s.recv(1024).decode()
print(msg)
```

Запрашиваем у пользователя данные и отправляем их на сервер. После чего выводим ответ от сервера.
```python
data = input().encode()
s.send(data)
print(s.recv(1024).decode())
```

***

## Задание #3

### Описание
Реализовать серверную часть приложения. Клиент подключается к серверу. В ответ
клиент получает http-сообщение, содержащее html-страницу, которую сервер
подгружает из файла index.html.

- Обязательно использовать библиотеку `socket`

### Решение

**Сервер**

Создаем TCP сокет с привязкой к данному хосту. Когда приходит соединение, отправляем http ответ клиенту.
```python
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 3001))
s.listen(1)

conn, addr = s.accept()
http_data = create_http_response(open("./index.html").read())
conn.sendall(http_data)
conn.close()
```

Функция, формирующая http ответ.
```python
def create_http_response(body: str) -> bytes:
  header = f"HTTP/1.2 200 OK\nContent-Type: text/html; charset=utf-8\nContent-Length: {len(body)}"
  request = f"{header}\n\n{body}"
  return request.encode()
```

**Клиент**

Соединяемся с TCP сервером и обрабатываем ответ.
```python
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('', 3001))

data = read_server_data(s)
body = read_http_body(data)

print(body)
```

Функция, читающая ответ с сервера по чанкам
```python
def read_server_data(s: socket.socket, chunk_size=1024) -> bytes:
  result = b""
  while True:
    data = s.recv(chunk_size)
    if not data:
      break
    result += data
  return result
```

Функция, которая выводит body с http ответа сервера.
```python
def read_http_body(response: bytes) -> str:
  lines = response.decode().splitlines()
  body_start = next((i for i, line in enumerate(lines) if line == ""), -1)
  if body_start == -1:
    raise ValueError("Invalid HTTP")
  return "\n".join(lines[body_start + 1:])
```

***

## Задание #4

### Описание
Реализовать двухпользовательский или многопользовательский чат. Реализация
многопользовательского чата позволяет получить максимальное количество
баллов.

- Реализовать с помощью протокола TCP – 100% баллов, с помощью UDP – 80%.
- Обязательно использовать библиотеку `threading`.
- Для реализации с помощью UDP, thearding использовать для получения
сообщений у клиента.
- Для применения с TCP необходимо запускать клиентские подключения И прием
и отправку сообщений всем юзерам на сервере в потоках. Не забудьте сохранять юзеров,
чтобы потом отправлять им сообщения.

### Решение

**Сервер**

Импортируем библиотеки.

```python
import os
import socket
from threading import Thread
from constants import separator
```

Основная часть серверной части кода. После создания TCP сервера, объявляем переменную connections, в которой будем хранить все соединения. Для каждого пользователя открываем отдельный thread для прослушивания его сообщений. 
```python
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# make port reusable
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', 3001))
s.listen(os.cpu_count())

connections: set[socket.socket] = set()
while True:
  conn, addr = s.accept()
  print(f"{addr} has connected.")
  connections.add(conn)

  # thread for listening client's messages
  t = Thread(target=listen_for_client, args=(conn,))
  t.start()
```

Функция прослушивания сообщений пользователей. После получения сообщения, каждому подключенному клиенту отправляется полученное сообщение.
```python
def listen_for_client(conn):
  global connections

  while True:
    try:
      msg = conn.recv(1024).decode()
    except Exception as e:
      # client no longer connected
      print(f"client no longer connected.")
      connections.remove(conn)
    else:
      msg = msg.replace(separator, ": ")

    # iterate over all connected sockets
    for client_socket in connections:
      client_socket.sendall(msg.encode())
```

**Клиент**

```python
import socket
import random
from threading import Thread
from datetime import datetime
from colorama import Fore
from constants import separator, colors
```

В основной части подклбчаемся к TCP серверу. Определяем цвет для пользователя, чтобы в чате сообщения выделялись определенным цветом. Запрашиваем его имя. После чего, создаем thread, в котором данный клиент будет получать сообщения от сервера.
```python
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('', 3001))

# choose a random color for the client
user_color = random.choice(colors)
username = input("Enter your name: ")

# make a thread that listens for messages to this client & print them
t = Thread(target=listen_for_messages, args=(s,))
t.start()
```

В этой функции идет вывод полученных ретранслированных сообщений от сервера. 
```python
def listen_for_messages(s: socket):
  try:
    while True:
      msg = s.recv(1024).decode()
      print(msg)
  finally:
    s.close()
```

Данный код обрабатывает отправку сообщений от данного клиента.
```python
while True:
  msg = input()

  if msg.lower() == '/exit':
    break

  date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

  s.sendall(f"{user_color}[{date_now}] {username}{separator}{msg}{Fore.RESET}".encode())
```

***

## Задание #5

### Описание
Необходимо написать простой web-сервер для обработки GET и POST http
запросов средствами Python и библиотеки socket.

Задание - сделать сервер, который может:

- Принять и записать информацию о дисциплине и оценке по дисциплине.
- Отдать информацию обо всех оценах по дсициплине в виде html-страницы.

### Решение

Определяем дата-классы, которые представляют из себя http-запрос и http-ответ. Для хранения оценок о предмете будем использовать defaultdict из библиотеки `collections`.
```python
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
```

Определяем конструктор класса, в котором также инициализируем сокет с протоколом TCP. Для того, чтобы запустить данный сервер используется функция `serve_forever`, в которой уже биндится хост и порт. Все соединения которые сервер принимает обрабатывает функция `serve_client`.
```python
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
```

В `parse_request` мы просто обрабатываем данные и приводим в нужный нам вид `HTTPRequest`.
```python
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
```

`parse_headers` обрабатывает заголовки.
```python
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
```

Данный метод обрабатывает запрос. В нем содержится вся бизнес-логика данного сервера. В качестве возвращаемых данных - собранный `HTTPResponse`.
```python
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
```

Так присходит запуск сервера.
```python
server = MyHTTPServer("localhost", 3004)
try:
  server.serve_forever()
except KeyboardInterrupt:
  pass
```

Посмотреть оценки по дисциплину.
```
GET /scores?subject=test
```

Внести оценки по дисциплину.
```
POST /subject?name=test&score=10
```