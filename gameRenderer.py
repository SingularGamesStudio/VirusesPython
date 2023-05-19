import pygame
from globals import *


class GameRenderer:
    width = 0
    height = 0
    scale = 1
    buttonScale = 2
    show = False

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
        self.markColor = (204, 181, 219)
        self.deadColor = (200, 200, 200)

    def renderGame(self, game, screen, rect):
        global SPRITE_SZ, OFFSET
        for i in range(game.size):
            for j in range(game.size):
                curRect = pygame.Rect(
                    rect.left+i*(SPRITE_SZ*self.scale+OFFSET)+OFFSET, rect.top+j*(SPRITE_SZ*self.scale+OFFSET)+OFFSET, SPRITE_SZ*self.scale, SPRITE_SZ*self.scale)
                img = self.emptySprite.copy()
                pixels = pygame.PixelArray(img)
                color = self.replaceColor
                if self.show and game.legal[i][j] and (not game.finished):
                    color = self.markColor
                pixels.replace(self.replaceColor, color)
                del pixels
                screen.blit(img, curRect)
                if (game.field[i][j].owner != -1):
                    img = self.aliveSprite.copy()
                    pixels = pygame.PixelArray(img)
                    color = self.playerColors[game.field[i]
                                              [j].owner] if game.alive[game.field[i][j].owner] else self.deadColor
                    pixels.replace(self.replaceColor, color)
                    del pixels
                    screen.blit(img, curRect)
                if (game.field[i][j].killer != -1):
                    img = self.killSprite.copy()
                    pixels = pygame.PixelArray(img)
                    color = self.playerColors[game.field[i]
                                              [j].killer] if game.alive[game.field[i][j].killer] else self.deadColor
                    pixels.replace(self.replaceColor, color)
                    del pixels
                    screen.blit(img, curRect)

    def renderText(self, game, screen):
        global SPRITE_SZ

        images = [pygame.image.load(
            'sprites/text/player.png'), pygame.image.load('sprites/text/'+str(game.curPlayer+1)+'.png')]
        if game.finished:
            images.append(pygame.image.load('sprites/text/win.png'))
        else:
            images.append(pygame.image.load('sprites/text/turn(.png'))
            images.append(pygame.image.load('sprites/text/' +
                          str(game.remainingActions)+'.png'))
            images.append(pygame.image.load('sprites/text/).png'))
        len = 0
        for img in images:
            len += img.get_width()
        len *= self.buttonScale
        left = (self.width-len)//2
        top = self.height-SPRITE_SZ*self.buttonScale
        for img in images:
            img = pygame.transform.scale(
                img, (img.get_width()*self.buttonScale, img.get_height()*self.buttonScale))
            pixels = pygame.PixelArray(img)
            color = self.playerColors[game.curPlayer]
            pixels.replace(self.replaceColor, color)
            del pixels
            screen.blit(img, pygame.Rect(
                left, top, img.get_width(), img.get_height()))
            left += img.get_width()
