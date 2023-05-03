import pygame_widgets
from pygame_widgets.button import Button
import pygame
from game import Game
from globals import *
from client import Client
from pygame_widgets.widget import WidgetHandler
from TextInputBox import TextInputBox
from gameRenderer import GameRenderer


class ButtonManager:
    buttons = {}
    newParams = {"players": 2,
                 "size": 14,
                 }
    inputBoxes = None
    groups = None
    active = [False]*4

    playerNamesOut = [""]*4
    playerCntOut = 2
    sizeOut = 10
    loginText = ""
    passwordText = ""

    def tickTextBoxes(self, events, screen):
        if self.net.state == "connecting" or self.net.state == "logging_in" or self.net.state == "requested_match":
            text_surface = self.font.render(
                self.net.state+"...", False, (255, 255, 255))
            screen.blit(text_surface, ((self.renderer.width-300)/2, 0))
        if self.net.state == "error":
            text_surface = self.font.render(
                self.net.last_error, False, (255, 255, 255))
            screen.blit(text_surface, ((self.renderer.width-300)/2, 0))
        if self.net.state == "login_window":
            text_surface = self.font.render('Login', False, (255, 255, 255))
            screen.blit(text_surface, ((self.renderer.width-300)/2, 0))
            text_surface = self.font.render('Password', False, (255, 255, 255))
            screen.blit(text_surface, ((self.renderer.width-300)/2, 100))
        if self.net.state == "starting_match":
            text_surface = self.font.render('Player 1', False, (255, 255, 255))
            screen.blit(text_surface, ((self.renderer.width-300)/2, 0))
            if self.active[1]:
                text_surface = self.font.render(
                    'Player 2', False, (255, 255, 255))
                screen.blit(text_surface, ((self.renderer.width-300)/2, 100))
                text_surface = self.font.render(
                    'Player 3', False, (255, 255, 255))
                screen.blit(text_surface, ((self.renderer.width-300)/2, 200))
        for i in range(4):
            if self.active[i]:
                self.groups[i].update(events)
                self.groups[i].draw(screen)

    def __init__(self, screen, renderer, game, net):
        global SPRITE_SZ, OFFSET
        self.renderer = renderer
        self.game = game
        self.net = net
        self.screen = screen
        sz = SPRITE_SZ*self.renderer.buttonScale
        self.newParams["players"] = self.game.players
        self.newParams["size"] = self.game.size
        self.backColor = (0, 0, 0)
        self.font = pygame.font.SysFont(None, 50)
        self.inputBoxes = [TextInputBox(
            (renderer.width-300)/2, 50+100*i, 300, self.font) for i in range(4)]
        self.groups = [pygame.sprite.Group(
            self.inputBoxes[i]) for i in range(4)]
        self.active = [False]*4

        for key in self.buttons:
            WidgetHandler.removeWidget(self.buttons[key])
        self.buttons.clear()

        if net.state == "main_menu":
            self.buttons["local"] = Button(
                screen,
                (renderer.width-300)/2,
                0,
                150,
                200,
                text="Local game",
                onClick=self.startLocal
            )
            self.buttons["online"] = Button(
                screen,
                (renderer.width-300)/2+150,
                0,
                150,
                200,
                text="Online game",
                onClick=self.startOnline
            )
        elif net.state == "connecting" or net.state == "logging_in" or net.state == "requested_match" or net.state == "error":
            self.buttons["cancel"] = Button(
                screen,
                (renderer.width-200)/2,
                200,
                200,
                200,
                text="Cancel",
                onClick=self.menu
            )
        elif net.state == "login_window":
            self.active[0] = True
            self.active[1] = True
            self.buttons["OK"] = Button(
                screen,
                (renderer.width-300)/2,
                200,
                150,
                50,
                text="OK",
                onClick=self.login
            )
            self.buttons["cancel"] = Button(
                screen,
                (renderer.width-300)/2+150,
                200,
                150,
                50,
                text="Cancel",
                onClick=self.menu
            )
        elif net.state == "starting_match":
            self.buttons["players"] = Button(
                screen,
                0,
                2*OFFSET,
                sz,
                sz,

                inactiveColour=self.backColor,
                image=self.getButtonImage(
                    str(self.newParams["players"])+"plr"),
                onClick=self.changePlayers
            )
            self.changePlayers()
            self.buttons["size"] = Button(
                screen,
                0,
                1*sz+4*OFFSET,
                sz,
                sz,

                inactiveColour=self.backColor,
                image=self.getButtonImage(str(game.size)+"x"+str(game.size)),
                onClick=self.resize
            )
            self.buttons["start"] = Button(
                screen,
                (renderer.width-300)/2,
                300,
                300,
                50,

                text="Start",
                onClick=self.requestStart
            )
        else:
            if net.state == "local_game":
                self.buttons["players"] = Button(
                    screen,
                    0,
                    2*OFFSET,
                    sz,
                    sz,

                    inactiveColour=self.backColor,
                    image=self.getButtonImage(
                        str(self.newParams["players"])+"plr"),
                    onClick=self.changePlayers
                )
                self.buttons["size"] = Button(
                    screen,
                    0,
                    1*sz+4*OFFSET,
                    sz,
                    sz,

                    inactiveColour=self.backColor,
                    image=self.getButtonImage(
                        str(game.size)+"x"+str(game.size)),
                    onClick=self.resize
                )
                self.buttons["apply"] = Button(
                    screen,
                    0,
                    2*sz+6*OFFSET,
                    sz,
                    sz,

                    inactiveColour=self.backColor,
                    image=self.getButtonImage("reset"),
                    onClick=self.apply
                )
            self.buttons["show"] = Button(
                screen,
                0,
                3*sz+8*OFFSET,
                sz,
                sz,

                inactiveColour=self.backColor,
                image=self.getButtonImage(
                    "visible") if self.renderer.show else self.getButtonImage("hidden"),
                onClick=self.show
            )

            self.buttons["scale"] = Button(
                screen,
                self.renderer.width-sz,
                2*OFFSET,
                sz,
                sz,

                inactiveColour=self.backColor,
                image=self.getButtonImage(
                    "upscale") if self.renderer.scale == 1 else self.getButtonImage("downscale"),
                onClick=self.resizeScreen
            )

            self.buttons["menu"] = Button(
                screen,
                self.renderer.width-sz,
                1*sz+4*OFFSET,
                sz,
                sz,

                text="MENU",
                onClick=self.menu
            )

            self.buttons["undo"] = Button(
                screen,
                self.renderer.width-sz,
                2*sz+6*OFFSET,
                sz,
                sz,

                inactiveColour=self.backColor,
                image=self.getButtonImage("undo"),
                onClick=self.undo
            )
            self.buttons["concede"] = Button(
                screen,
                self.renderer.width-sz,
                3*sz+8*OFFSET,
                sz,
                sz,

                inactiveColour=self.backColor,
                image=self.getButtonImage("concede"),
                onClick=self.concede
            )

    def getButtonImage(self, s):
        global SPRITE_SZ
        path = 'sprites/buttons/'+s+'.png'
        img = pygame.image.load(path)
        img = pygame.transform.scale(
            img, (SPRITE_SZ*self.renderer.buttonScale, SPRITE_SZ*self.renderer.buttonScale))
        return img

    def apply(self):
        self.game.__init__(
            self.newParams["size"], self.newParams["players"])
        self.renderer.__init__(self.game.size)
        self.screen = pygame.display.set_mode(
            (self.renderer.width, self.renderer.height))
        self.__init__(self.screen, self.renderer, self.game, self.net)

    def changePlayers(self):
        if (self.newParams["players"] == 2):
            self.newParams["players"] = 4
            self.active = [True]*3
            self.active.append(False)
            self.buttons["players"].image = self.getButtonImage("4plr")
        else:
            self.newParams["players"] = 2
            self.active = [True]
            self.active.append(False)
            self.active.append(False)
            self.active.append(False)
            self.buttons["players"].image = self.getButtonImage("2plr")

    def resize(self):
        sizes = [8, 10, 12, 14]
        id = 0
        for i in range(len(sizes)):
            if self.newParams["size"] == sizes[i]:
                id = i
        sz = sizes[(id+1) % len(sizes)]
        self.newParams["size"] = sz
        self.buttons["size"].image = self.getButtonImage(str(sz)+"x"+str(sz))

    def resizeScreen(self):
        if (self.renderer.scale == 1):
            self.renderer.scale = 2
            self.renderer.buttonScale = 4
            self.buttons["scale"].image = self.getButtonImage("downscale")
        else:
            self.renderer.scale = 1
            self.renderer.buttonScale = 2
            self.buttons["scale"].image = self.getButtonImage("upscale")
        self.renderer.__init__(self.game.size)
        self.screen = pygame.display.set_mode(
            (self.renderer.width, self.renderer.height))
        self.__init__(self.screen, self.renderer, self.game, self.net)

    def undo(self):
        self.game.undo()

    def concede(self):
        if self.game.id == -1:
            self.game.die()
        else:
            self.net.sock.send(str.encode(
                "concede "+str(self.game.id)+" "+str(self.game.myPlayer)))

    def show(self):
        self.renderer.show = not self.renderer.show
        self.buttons["show"].image = self.getButtonImage(
            "visible") if self.renderer.show else self.getButtonImage("hidden")

    def startLocal(self):
        self.net.state = "local_game"
        self.game.__init__(10, 2)

    def startOnline(self):
        self.net.state = "connecting"

    def menu(self):
        self.net.state = "main_menu"

    def login(self):
        self.net.state = "logging_in"
        self.loginText = self.inputBoxes[0].text
        self.passwordText = self.inputBoxes[1].text

    def requestStart(self):
        self.net.state = "requested_match"
        for i in range(4):
            self.playerNamesOut[i] = self.inputBoxes[i].text
        self.playerCntOut = self.newParams["players"]
        self.sizeOut = self.newParams["size"]
