class Node:
    owner = -1
    killer = -1

    def __init__(self, owner=-1):
        self.owner = owner

    def go(self, player):
        if self.owner == -1:
            self.owner = player
            self.killer = -1
        elif self.owner != player:
            self.killer = player
        else:
            raise Exception("cannot make turn in your own cell")

    def undo(self):
        if self.killer != -1:
            self.killer = -1
        else:
            self.owner = -1


class Game:
    net = None

    def __init__(self, sz=0, players=0):
        if sz == 0 or players == 0:
            return
        self.finished = False
        self.id = -1
        self.myPlayer = 0
        self.turns = [(0, 0), (0, 0), (0, 0)]
        if players != 2 and players != 4:
            raise Exception("there could only be 2 or 4 players")
        if (sz < 4):
            raise Exception("size must be at least 4")
        self.players = players
        self.alive = [True]*players
        self.size = sz
        self.field = [[Node() for i in range(sz)] for j in range(sz)]
        self.field[sz-1][0] = Node(0)
        self.field[0][sz-1] = Node(1)
        if players == 4:
            self.field[0][0] = Node(2)
            self.field[sz-1][sz-1] = Node(3)
        self.curPlayer = 0
        self.remainingActions = 3
        self.updateLegal()

    def updateLegal(self):
        self.legal = [[False for i in range(self.size)]
                      for j in range(self.size)]
        used = [[False for i in range(self.size)] for j in range(self.size)]
        stack = []
        for x in range(self.size):
            for y in range(self.size):
                if self.field[x][y].killer == -1 and self.field[x][y].owner == self.curPlayer:
                    stack.append((x, y))
                    used[x][y] = True
        cnt = 0
        while len(stack) > 0:
            pos = stack.pop()
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    pos1 = (pos[0]+dx, pos[1]+dy)
                    if (not (dx == 0 and dy == 0)) and (pos1[0] >= 0 and pos1[0] < self.size) and (pos1[1] >= 0 and pos1[1] < self.size):
                        if not used[pos1[0]][pos1[1]]:
                            if self.field[pos1[0]][pos1[1]].killer == self.curPlayer:
                                stack.append((pos1[0], pos1[1]))
                            elif self.field[pos1[0]][pos1[1]].killer == -1:
                                self.legal[pos1[0]][pos1[1]] = True
                                cnt += 1
                            used[pos[0]+dx][pos[1]+dy] = True
        if cnt == 0:
            if self.id != -1:
                if self.curPlayer == self.myPlayer:
                    self.net.sock.send(str.encode(
                        "concede "+str(self.id)+" "+str(self.myPlayer)))
            self.die()

    def go(self, x, y):
        if not self.finished:
            if not self.legal[x][y]:
                raise Exception("cannot make this move")
            else:
                self.field[x][y].go(self.curPlayer)
            self.turns[3-self.remainingActions] = (x, y)
            self.remainingActions -= 1
            if self.remainingActions == 0:
                if self.id != -1 and self.curPlayer == self.myPlayer:
                    self.net.sock.send(str.encode("go "+str(self.id)+" "+str(self.turns[0][0])+" "+str(self.turns[0][1])+" "+str(
                        self.turns[1][0])+" "+str(self.turns[1][1])+" "+str(self.turns[2][0])+" "+str(self.turns[2][1])))
                self.remainingActions = 3
                self.curPlayer = (self.curPlayer+1) % self.players
                while not self.alive[self.curPlayer]:
                    self.curPlayer = (self.curPlayer+1) % self.players
            self.updateLegal()

    def undo(self):
        if (not self.finished) and self.remainingActions != 3:
            self.remainingActions += 1
            pos = self.turns[3-self.remainingActions]
            self.field[pos[0]][pos[1]].undo()
            self.updateLegal()

    def die(self, player=-2):
        if player == -2:
            player = self.curPlayer
        if not self.finished:
            if player == self.curPlayer:
                self.remainingActions = 3
            self.alive[player] = False
            cnt = 0
            for i in range(self.players):
                if self.alive[i]:
                    cnt += 1
            while not self.alive[self.curPlayer]:
                self.curPlayer = (self.curPlayer+1) % self.players
            if cnt == 1:
                self.finished = True
            else:
                self.updateLegal()
