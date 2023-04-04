import pygame
import random
from globals import *
from gameRenderer import GameRenderer
from game import Game


def draw(screen, game, renderer, backgroundRect):
    global SPRITE_SZ, OFFSET

    pygame.draw.rect(screen, (100, 100, 100), backgroundRect)
    renderer.render(game, screen, backgroundRect)


def main():
    global WIDTH, HEIGHT, FPS
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    game = Game(10, 2)
    renderer = GameRenderer()
    currentPlayer = 0
    actions = 3

    running = True
    while running:
        clock.tick(FPS)
        BACK_SZ = game.size*(SPRITE_SZ+OFFSET) + OFFSET
        backgroundRect = pygame.Rect(0, 0, BACK_SZ, BACK_SZ)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if backgroundRect.collidepoint(event.pos):
                    x = event.pos[0]//(SPRITE_SZ+OFFSET)
                    y = event.pos[1]//(SPRITE_SZ+OFFSET)
                    try:
                        game.go(x, y)
                    except:
                        print("wrong move")
        draw(screen, game, renderer, backgroundRect)
        pygame.display.flip()


main()
