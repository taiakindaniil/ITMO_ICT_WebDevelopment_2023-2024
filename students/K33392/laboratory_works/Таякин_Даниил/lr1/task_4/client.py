import socket
import random
from threading import Thread
from datetime import datetime
from colorama import Fore
from constants import separator, colors


def listen_for_messages(s: socket):
  try:
    while True:
      msg = s.recv(1024).decode()
      print(msg)
  finally:
    s.close()


if __name__ == "__main__":
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect(('', 3001))

  # choose a random color for the client
  user_color = random.choice(colors)
  username = input("Enter your name: ")

  # make a thread that listens for messages to this client & print them
  t = Thread(target=listen_for_messages, args=(s,))
  t.start()

  while True:
    msg = input()

    if msg.lower() == '/exit':
      break

    date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    s.sendall(f"{user_color}[{date_now}] {username}{separator}{msg}{Fore.RESET}".encode())