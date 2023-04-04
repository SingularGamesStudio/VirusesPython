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


class Game:

    def __init__(self, sz, players):
        if players != 2 and players != 4:
            raise Exception("there could only be 2 or 4 players")
        if (sz < 4):
            raise Exception("size must be at least 4")
        self.players = players
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
                            used[pos[0]+dx][pos[1]+dy] = True

    def go(self, x, y):
        if not self.legal[x][y]:
            raise Exception("cannot make this move")
        else:
            self.field[x][y].go(self.curPlayer)
        self.remainingActions -= 1
        if self.remainingActions == 0:
            self.remainingActions = 3
            self.curPlayer = (self.curPlayer+1) % self.players
        self.updateLegal()
