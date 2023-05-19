import sys
import socket
import selectors
import types
from game import Game


class Server:
    selector = selectors.DefaultSelector()
    database = {}
    connected = {}

    games = {}
    gameid = 0

    mySocket = None

    def __init__(self):
        host = "127.0.0.1"
        port = 7777
        with open("address.ini") as file:
            host = file.read().split()
            port = int(host[1])
            host = host[0]
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
            address=address, player="")
        self.selector.register(connection, selectors.EVENT_READ, data=data)

    def eval(self, rec, data, sock):
        items = rec.split()
        if items[0] == b"auth":
            if not (items[1] in self.database):
                print(data.address, "auth as", items[1], items[2])
                self.database[items[1]] = items[2]

                self.connected[items[1]] = sock
                data.player = items[1]
                sock.send(str.encode("auth_success"))
            elif self.database[items[1]] == items[2]:
                print(data.address, "auth as", items[1], items[2])

                self.connected[items[1]] = sock
                data.player = items[1]
                sock.send(str.encode("auth_success"))
            else:
                sock.send(str.encode("auth_denied"))
        if items[0] == b"start":
            sz = int(items[1])
            playercnt = int(items[2])
            host = data.player
            players = []
            ok = True
            for i in range(playercnt-1):
                if 3+i < len(items):
                    players.append(items[3+i])
                    if not (items[3+i] in self.connected.keys()):
                        sock.send(str.encode("stop_game player_offline"))
                        ok = False
                        break
                else:
                    players.append("")
            print("game start requested by",
                  data.player, "with players", players)
            if ok:
                if len(self.connected) < playercnt-1:
                    sock.send(str.encode("stop_game too_few_players"))
                    ok = False
            if ok:
                print("looking for players")
                self.games[self.gameid] = types.SimpleNamespace(
                    host=host,
                    players=players,
                    sz=sz,
                    playercnt=playercnt,
                    id=self.gameid,
                    req=[],
                    ref=[],
                    acc=[],
                    dis=[]
                )
                self.gameid += 1
        if items[0] == b"accept":
            id = int(items[1])
            self.games[id].req.remove(data.player)
            self.games[id].acc.append(data.player)
        if items[0] == b"refuse":
            id = int(items[1])
            self.games[id].req.remove(data.player)
            self.games[id].ref.append(data.player)
        if items[0] == b"concede":
            for player in self.games[int(items[1])].acc:
                if player != data.player:
                    self.connected[player].send(
                        str.encode("concede "+str(int(items[2]))))
        if items[0] == b"go":
            for player in self.games[int(items[1])].acc:
                if player != data.player:
                    self.connected[player].send(rec)

    def closeGame(self, id, why):
        for s in self.games[id].acc:
            if s in self.connected.keys():
                self.connected[s].send(str.encode("stop_game "+why))
        if self.games[id].host in self.connected.keys():
            self.connected[self.games[id].host].send(
                str.encode("stop_game "+why))
        self.games.pop(id)

    def receive(self, key):
        sock = key.fileobj
        data = key.data
        rec = sock.recv(2048)
        if rec:
            self.eval(rec, data, sock)
        else:
            name = data.player
            if name != "":
                for id, game in self.games.items():
                    if game.host == name:
                        self.closeGame(id, "host_disconnect")
                        break
                    if name in game.req:
                        game.req.remove(name)
                        game.ref.append(name)
                    if name in game.acc:
                        game.acc.remove(name)
                        game.dis.append(name)

                self.connected.pop(name)
            print(data.address, "disconnected")
            self.selector.unregister(sock)
            sock.close()

    def tick(self):
        events = self.selector.select(timeout=0.01)
        for key, _ in events:
            if key.data is None:
                self.connect(key.fileobj)
            else:
                self.receive(key)
        toclose = []
        for id, game in self.games.items():
            # print(game.acc, game.players, game.ref, game.req)
            if game.host != "":
                if len(game.acc) == len(game.players):
                    game.acc.append(game.host)
                    game.host = ""
                    num = 0
                    for plr in game.acc:
                        self.connected[plr].send(str.encode(
                            "game_start "+str(game.id)+" "+str(game.sz)+" "+str(len(game.acc))+" "+str(num)))
                        num += 1
                    print("game starting")
                else:
                    if len(game.players) > len(game.acc)+len(game.req):
                        for name in game.players:
                            s = name
                            if name == "":
                                for plr, conn in self.connected.items():
                                    if plr in game.acc or plr in game.req or plr in game.ref or plr == game.host:
                                        continue
                                    s = plr
                                if s == "":
                                    print("not enough players online, aborting")
                                    toclose.append((id, "too_few_players"))
                            if name in game.acc or name in game.req:
                                continue
                            if s != "":
                                game.req.append(s)
                                if not s in self.connected.keys():
                                    print("player "+str(s) +
                                          " offline, aborting")
                                    toclose.append((id, "player_offline"))
                                else:
                                    self.connected[s].send(
                                        str.encode("req_game "+str(id)))
        for id, s in toclose:
            self.closeGame(id, s)


net = Server()

try:
    while True:
        net.tick()
except KeyboardInterrupt:
    net.mySocket.close()
