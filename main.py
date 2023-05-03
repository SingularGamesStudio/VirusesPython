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

    running = True
    game = Game(10, 2)
    net = Client(game)
    game.net = net
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
            if buttons.loginText == "" or buttons.passwordText == "":
                net.state = "error"
                net.last_error = "ERROR: Empty string"
            elif ' ' in buttons.loginText or ' ' in buttons.passwordText:
                net.state = "error"
                net.last_error = "ERROR: Space in str"
            else:
                buttons.tickTextBoxes(events, screen)
                if not net.authorize_requested:
                    net.authorize(buttons.loginText, buttons.passwordText)
                else:
                    if net.authorized:
                        net.state = "starting_match"
        elif net.state == "starting_match" or net.state == "error":
            buttons.tickTextBoxes(events, screen)
        elif net.state == "requested_match":
            if not net.match_requested:
                plrs = []
                sz = buttons.sizeOut
                for i in range(buttons.playerCntOut-1):
                    s = buttons.playerNamesOut[i]
                    if ' ' in s:
                        net.state = "error"
                        net.last_error = "ERROR: Space in str"
                    for j in range(i):
                        if buttons.playerNamesOut[i] == buttons.playerNamesOut[j]:
                            net.state = "error"
                            net.last_error = "ERROR: Same players"
                    if buttons.playerNamesOut[i] == net.login:
                        net.state = "error"
                        net.last_error = "ERROR: Same players"
                    plrs.append(s)
                if net.state != "error":
                    net.startGame(plrs, sz)
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
                            if game.id == -1 or game.myPlayer == game.curPlayer:
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
