import sys
import socket
import selectors
import types
from game import Game


class Server:
    selector = selectors.DefaultSelector()
    database = {}
    mySocket = None

    def __init__(self, host="127.0.0.1", port=7777):
        self.mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.mySocket.bind((host, port))
        self.mySocket.listen()
        print("Server running on", host, ":", port)
        self.mySocket.setblocking(False)
        self.selector.register(self.mySocket, selectors.EVENT_READ, data=None)

    def connect(self, sock):
        connection, address = sock.accept()
        print(address, "connected")
        connection.setblocking(False)
        data = types.SimpleNamespace(
            address=address, inb=b"", outb=b"", player=0)
        self.selector.register(connection, selectors.EVENT_READ, data=data)

    def eval(self, rec, data, sock):
        items = rec.split()
        if items[0] == b"auth":
            if not (items[1] in self.database):
                print(data.address, "auth as", items[1], items[2])
                self.database[items[1]] = items[2]
                sock.send(str.encode("auth_success"))
            elif self.database[items[1]] == items[2]:
                print(data.address, "auth as", items[1], items[2])
                sock.send(str.encode("auth_success"))
            else:
                sock.send(str.encode("auth_denied"))

    def receive(self, key):
        sock = key.fileobj
        data = key.data
        rec = sock.recv(2048)
        if rec:
            self.eval(rec, data, sock)
        else:
            print(data.address, "disconnected")
            self.selector.unregister(sock)
            sock.close()

    def tick(self):
        events = self.selector.select(timeout=None)
        for key, _ in events:
            if key.data is None:
                self.connect(key.fileobj)
            else:
                self.receive(key)


net = Server()

try:
    while True:
        net.tick()
except KeyboardInterrupt:
    net.mySocket.close()
