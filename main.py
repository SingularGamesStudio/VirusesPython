import pygame
from globals import *
from buttons import ButtonManager
from gameRenderer import GameRenderer
from game import Game
import pygame_widgets
from client import Client
from TextInputBox import TextInputBox


def getGameRect(renderer, gameSize):
    global SPRITE_SZ, OFFSET

    BACK_SZ = gameSize*(renderer.scale*SPRITE_SZ+OFFSET) + OFFSET
    backgroundRect = pygame.Rect(0, 0, BACK_SZ, BACK_SZ)
    backgroundRect.centerx = renderer.width/2
    backgroundRect.centery = BACK_SZ/2
    return backgroundRect


def main():
    net = Client()
    running = True
    game = Game(10, 2)
    pygame.init()
    clock = pygame.time.Clock()
    renderer = GameRenderer(10)
    screen = pygame.display.set_mode((renderer.width, renderer.height))
    laststate = "main_menu"
    sepColor = (100, 100, 100)
    backColor = (0, 0, 0)
    buttons = ButtonManager(screen, renderer, game, net)

    while running:
        screen.fill(backColor)
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                running = False
        net.tick()
        if (laststate != net.state):
            buttons.__init__(screen, renderer, game, net)
        laststate = net.state
        if net.state == "main_menu":
            pass
        elif net.state == "connecting":
            if not net.connected:
                net.reconnect()
            else:
                net.state = "login_window"
        elif net.state == "login_window":
            buttons.tickTextBoxes(events, screen)
        elif net.state == "logging_in":
            buttons.tickTextBoxes(events, screen)
            if net.authorize_rejected:
                net.authorize_rejected = False
                print("authorize not successful")
                net.state = "main_menu"
            elif not net.authorize_requested:
                net.authorize(buttons.loginText, buttons.passwordText)
            else:
                if net.authorized:
                    net.state = "starting_match"
        elif net.state == "starting_match":
            buttons.tickTextBoxes(events, screen)
        elif net.state == "requested_match":
            buttons.tickTextBoxes(events, screen)
        else:
            backgroundRect = getGameRect(renderer, game.size)
            for event in events:
                if event.type == pygame.MOUSEBUTTONUP:
                    if backgroundRect.collidepoint(event.pos):
                        x = (
                            event.pos[0]-backgroundRect.left)//(renderer.scale*SPRITE_SZ+OFFSET)
                        y = (
                            event.pos[1] - backgroundRect.top)//(renderer.scale*SPRITE_SZ+OFFSET)
                        try:
                            game.go(x, y)
                        except Exception as e:
                            print(e)
            pygame.draw.rect(screen, sepColor, backgroundRect)
            renderer.renderGame(game, screen, backgroundRect)
            renderer.renderText(game, screen)

        pygame_widgets.update(events)
        pygame.display.flip()
        clock.tick(FPS)


main()
