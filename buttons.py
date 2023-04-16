import pygame_widgets
from pygame_widgets.button import Button
import pygame
from game import Game
from globals import *
from pygame_widgets.widget import WidgetHandler


class ButtonManager:
    buttons = {}
    newParams = {"players": 2,
                 "size": 14,
                 }

    def __init__(self, screen, renderer, game):
        global SPRITE_SZ, OFFSET
        self.renderer = renderer
        self.game = game
        self.screen = screen
        sz = SPRITE_SZ*self.renderer.buttonScale
        self.newParams["players"] = self.game.players
        self.newParams["size"] = self.game.size

        for key in self.buttons:
            WidgetHandler.removeWidget(self.buttons[key])
        self.buttons["players"] = Button(
            screen,
            0,
            0,
            sz,
            sz,

            image=self.getButtonImage(
                str(self.newParams["players"])+"plr"),
            onClick=self.changePlayers
        )
        self.buttons["size"] = Button(
            screen,
            0,
            sz+OFFSET,
            sz,
            sz,

            image=self.getButtonImage(str(game.size)+"x"+str(game.size)),
            onClick=self.resize
        )
        self.buttons["apply"] = Button(
            screen,
            0,
            2*sz+2*OFFSET,
            sz,
            sz,

            image=self.getButtonImage("reset"),
            onClick=self.apply
        )

        self.buttons["scale"] = Button(
            screen,
            self.renderer.width-sz,
            0,
            sz,
            sz,

            image=self.getButtonImage(
                "upscale") if self.renderer.scale == 1 else self.getButtonImage("downscale"),
            onClick=self.resizeScreen
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
        self.__init__(self.screen, self.renderer, self.game)

    def changePlayers(self):
        if (self.newParams["players"] == 2):
            self.newParams["players"] = 4
            self.buttons["players"].image = self.getButtonImage("4plr")
        else:
            self.newParams["players"] = 2
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
            self.renderer.buttonScale = 3
            self.buttons["scale"].image = self.getButtonImage("downscale")
        else:
            self.renderer.scale = 1
            self.renderer.buttonScale = 2
            self.buttons["scale"].image = self.getButtonImage("upscale")
        self.renderer.__init__(self.game.size)
        self.screen = pygame.display.set_mode(
            (self.renderer.width, self.renderer.height))
        self.__init__(self.screen, self.renderer, self.game)
