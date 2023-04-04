import pygame
from globals import *


class GameRenderer:
    def __init__(self):
        self.emptySprite = pygame.image.load('sprites/empty.png')
        self.aliveSprite = pygame.image.load('sprites/alive.png')
        self.killSprite = pygame.image.load('sprites/killed.png')
        self.backgroundColor = (255, 255, 255)
        self.replaceColor = pygame.PixelArray(self.emptySprite)[0][0]
        self.playerColors = [(255, 0, 0), (0, 255, 0),
                             (0, 0, 255), (255, 255, 0)]

    def render(self, game, screen, rect):
        global SPRITE_SZ, OFFSET
        for i in range(game.size):
            for j in range(game.size):
                curRect = pygame.Rect(
                    rect.top+i*(SPRITE_SZ+OFFSET)+OFFSET, rect.left+j*(SPRITE_SZ+OFFSET)+OFFSET, SPRITE_SZ, SPRITE_SZ)
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
