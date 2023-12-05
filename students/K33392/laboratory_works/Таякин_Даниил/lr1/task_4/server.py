import os
import socket
from threading import Thread
from constants import separator


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


if __name__ == "__main__":
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
