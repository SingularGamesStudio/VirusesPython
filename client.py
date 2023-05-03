import sys
import socket
import selectors
import types


class Client:
    selector = selectors.DefaultSelector()

    sock = None
    game = None

    connected = False
    authorize_requested = False
    authorized = False
    match_requested = False

    login = ""

    state = "main_menu"
    last_error = ""

    def disconnect(self):
        self.sock.shutdown(socket.SHUT_RDWR)
        self.connected = False
        self.authorize_requested = False
        self.authorized = False

    def reconnect(self, host="127.0.0.1", port=7777):
        if self.connected:
            self.disconnect()
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
            self.login = login
            print("authorize requested")
        except Exception as e:
            pass

    def __init__(self, game):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setblocking(False)
        self.game = game

    def startGame(self, players, sz):
        request = "start "+str(sz)+" "+str(len(players)+1)
        for i in range(len(players)):
            request += " "+players[i]
        self.match_requested = False
        try:
            self.sock.send(str.encode(request))
            self.match_requested = True
        except:
            pass

    def eval(self, rec, data):
        items = rec.split()
        if items[0] == b"auth_success":
            self.authorized = True
            print("authorized")
        elif items[0] == b"auth_denied" and self.state == "logging_in":
            self.authorized = False
            self.authorize_requested = False
            self.state = "error"
            self.last_error = "ERROR: Wrong password"
        elif items[0] == b"req_game":
            if self.state == "starting_match":
                self.state = "requested_match"  # TODO: ask player whether they want to play
                self.match_requested = True
                print("accept")
                self.sock.send(str.encode("accept "+str(int(items[1]))))
            else:
                print("refuse")
                self.sock.send(str.encode("refuse "+str(int(items[1]))))
        elif items[0] == b"game_start":
            if self.state == "requested_match":
                self.state = "online_game"
                self.game.__init__(int(items[2]), int(items[3]))
                self.game.myPlayer = int(items[4])
                self.game.id = int(items[1])
            else:
                self.sock.send(str.encode("concede "+str(int(items[1]))))
        elif items[0] == b"stop_game":
            if self.state == "online_game" or self.state == "requested_match":
                self.state = "error"
                self.last_error = "ERROR: "+items[1]
        elif items[0] == b"concede" and self.state == "online_game":
            self.game.die(int(items[1]))
        elif items[0] == b"go":
            self.game.go(int(items[2]), int(items[3]))
            self.game.go(int(items[4]), int(items[5]))
            self.game.go(int(items[6]), int(items[7]))

    def receive(self, key, mask):
        sock = key.fileobj
        data = key.data
        rec = sock.recv(2048)
        print(rec)
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
