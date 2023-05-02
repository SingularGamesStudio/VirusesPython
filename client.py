import sys
import socket
import selectors
import types


class Client:
    selector = selectors.DefaultSelector()

    sock = None

    connected = False
    authorize_requested = False
    authorized = False
    authorize_rejected = False

    state = "main_menu"

    def reconnect(self, host="127.0.0.1", port=7777):
        if self.connected:
            self.sock.close()
            self.connected = False
            self.authorize_requested = False
            self.authorized = False
        try:
            self.sock.connect((host, port))
            self.selector.register(self.sock, selectors.EVENT_READ, data=True)
            self.connected = True
            print("connected to server")
        except:
            pass

    def authorize(self, login, password):
        try:
            self.sock.send(str.encode("auth "+login+" "+password))
            self.authorize_requested = True
            self.authorize_rejected = False
            print("authorize requested")
        except Exception as e:
            pass

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setblocking(False)

    def eval(self, rec, data):
        items = rec.split()
        if items[0] == b"auth_success":
            self.authorized = True
            print("authorized")
        elif items[0] == b"auth_denied":
            self.authorized = False
            self.authorize_requested = False
            self.authorize_rejected = True

    def receive(self, key, mask):
        sock = key.fileobj
        data = key.data
        rec = sock.recv(2048)
        if rec:
            self.eval(rec, data)
        else:
            print("connection lost")
            self.reconnect()

    def tick(self):
        events = self.selector.select(timeout=0.01)
        for key, mask in events:

            self.receive(key, mask)


'''
net = Client()

try:
    while True:
        while (not net.connected):
            net.reconnect()

        while (not net.authorize_requested):
            net.authorize("biba", "abacaba")

        net.tick()
except KeyboardInterrupt:
    net.sock.close()
'''
