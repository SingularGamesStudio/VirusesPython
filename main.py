import pygame
from globals import *
from buttons import ButtonManager
from gameRenderer import GameRenderer
from game import Game
import pygame_widgets


def getGameRect(renderer, gameSize):
    global SPRITE_SZ, OFFSET

    BACK_SZ = gameSize*(renderer.scale*SPRITE_SZ+OFFSET) + OFFSET
    backgroundRect = pygame.Rect(0, 0, BACK_SZ, BACK_SZ)
    backgroundRect.centerx = renderer.width/2
    backgroundRect.centery = BACK_SZ/2
    return backgroundRect


def main():
    game = Game(10, 2)
    pygame.init()
    clock = pygame.time.Clock()
    renderer = GameRenderer(game.size)
    screen = pygame.display.set_mode((renderer.width, renderer.height))
    buttons = ButtonManager(screen, renderer, game)
    sepColor = (100, 100, 100)
    backColor = (0, 0, 0)

    running = True
    while running:
        clock.tick(FPS)
        backgroundRect = getGameRect(renderer, game.size)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                if backgroundRect.collidepoint(event.pos):
                    x = (
                        event.pos[0]-backgroundRect.left)//(renderer.scale*SPRITE_SZ+OFFSET)
                    y = (
                        event.pos[1] - backgroundRect.top)//(renderer.scale*SPRITE_SZ+OFFSET)
                    try:
                        game.go(x, y)
                    except Exception as e:
                        print(e)

        screen.fill(backColor)
        pygame.draw.rect(screen, sepColor, backgroundRect)
        renderer.renderGame(game, screen, backgroundRect)
        renderer.renderText(game, screen)
        pygame_widgets.update(events)

        pygame.display.flip()


main()
