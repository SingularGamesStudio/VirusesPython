import pygame
from globals import *


class GameRenderer:
    width = 0
    height = 0
    scale = 1
    buttonScale = 2

    def __init__(self, gameSize):
        global SPRITE_SZ, OFFSET

        self.height = (SPRITE_SZ*self.scale+OFFSET) * \
            gameSize+OFFSET+SPRITE_SZ*self.buttonScale
        self.width = (SPRITE_SZ*self.scale+OFFSET)*gameSize + \
            OFFSET+SPRITE_SZ*self.buttonScale*2

        self.emptySprite = pygame.transform.scale(
            pygame.image.load('sprites/empty.png'), (SPRITE_SZ*self.scale, SPRITE_SZ*self.scale))
        self.aliveSprite = pygame.transform.scale(
            pygame.image.load('sprites/alive.png'), (SPRITE_SZ*self.scale, SPRITE_SZ*self.scale))
        self.killSprite = pygame.transform.scale(
            pygame.image.load('sprites/killed.png'), (SPRITE_SZ*self.scale, SPRITE_SZ*self.scale))
        self.backgroundColor = (255, 255, 255)
        self.replaceColor = pygame.PixelArray(self.emptySprite)[0][0]
        self.playerColors = [(255, 0, 0), (0, 255, 0),
                             (0, 0, 255), (255, 255, 0)]

    def renderGame(self, game, screen, rect):
        global SPRITE_SZ, OFFSET
        for i in range(game.size):
            for j in range(game.size):
                curRect = pygame.Rect(
                    rect.left+i*(SPRITE_SZ*self.scale+OFFSET)+OFFSET, rect.top+j*(SPRITE_SZ*self.scale+OFFSET)+OFFSET, SPRITE_SZ*self.scale, SPRITE_SZ*self.scale)
                screen.blit(self.emptySprite, curRect)
                if (game.field[i][j].owner != -1):
                    img = self.aliveSprite.copy()
                    pixels = pygame.PixelArray(img)
                    pixels.replace(self.replaceColor,
                                   self.playerColors[game.field[i][j].owner])
                    del pixels
                    screen.blit(img, curRect)
                if (game.field[i][j].killer != -1):
                    img = self.killSprite.copy()
                    pixels = pygame.PixelArray(img)
                    pixels.replace(self.replaceColor,
                                   self.playerColors[game.field[i][j].killer])
                    del pixels
                    screen.blit(img, curRect)
