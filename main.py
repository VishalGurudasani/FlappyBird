import random  # for generating random numbers
import sys  # to exit the game
import pygame
from pygame.locals import *

# global variable for game
FPS = 10
SCREENWIDTH = 600
SCREENHEIGHT = 500
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.7
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'sprites/bird.png'
BACKGROUND = 'sprites/background.png'
PIPE = 'sprites/pipe.png'


def welcomescreen():
    # shows the message PNG on screen

    x = int(SCREENWIDTH/5)
    y = int((SCREENHEIGHT - GAME_SPRITES['PLAYER'].get_height())/2)
    messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width())/2)
    messagey = int(SCREENHEIGHT*0.1)
    basex = 0
    while True:
        for event in pygame.event.get():
            # for closing the game
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # for starting the game
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['BACKGROUND'], (0, 0))
                SCREEN.blit(GAME_SPRITES['PLAYER'], (x, y))
                SCREEN.blit(GAME_SPRITES['message'], (messagex, messagey))
                SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)


def maingame():
    score = 0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENWIDTH/2)
    basex = 0

    # create two pipes
    newpipe1 = getRandompipe()
    newpipe2 = getRandompipe()

    # list of upper and lower pipes
    upperpipes = [
        {'x': SCREENWIDTH + 200, 'y': newpipe1[0]['y']},
        {'x': SCREENWIDTH + SCREENWIDTH/2 + 100, 'y': newpipe2[0]['y']},
    ]

    lowerpipes = [
        {'x': SCREENWIDTH + 200, 'y': newpipe1[1]['y']},
        {'x': SCREENWIDTH + SCREENWIDTH/2 + 200, 'y': newpipe2[1]['y']},
    ]

    pipevelx = -4
    playervely = -9
    playermaxvely = 10
    playerminvely = -8
    playeraccuracy = 1
    playerflapvel = -8  # vel while flapping
    playerflapped = False  # true when the bird is flapping

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playervely = playerflapvel
                    playerflapped = True
                    GAME_SOUNDS['wings'].play()

        # function return true if player is crashed
        crashtest = collide(playerx, playery, upperpipes, lowerpipes)
        if crashtest:
            return True

        # check score
        playermidpos = playerx + GAME_SPRITES['PLAYER'].get_width()/2
        for pipe in upperpipes:
            pipemidpos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipemidpos <= playermidpos < pipemidpos + 5:
                score += 1
                print(f"your score is{score}")
                GAME_SOUNDS['point'].play()

            if playervely < playermaxvely and not playerflapped:
                playervely += playeraccuracy

            if playerflapped:
                playerflapped = False
            playerheight = GAME_SPRITES['PLAYER'].get_height()
            playery = playery + \
                min(playervely, GROUNDY - playery - playerheight)

        # move pipes to the left
        for upperpipe, lowerpipe in zip(upperpipes, lowerpipes):
            upperpipe['x'] += pipevelx
            lowerpipe['x'] += pipevelx

        # add a new pipe before removing it
        if 0 < upperpipe['x'] < 5:
            newpipe = getRandompipe()
            upperpipes.append(newpipe[0])
            lowerpipes.append(newpipe[1])

        # if pipe is out of the screen remove it
        if upperpipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperpipes.pop(0)
            lowerpipes.pop(0)

        # let blit the sprites now
        SCREEN.blit(GAME_SPRITES['BACKGROUND'], (0, 0))
        for upperpipe, lowerpipe in zip(upperpipes, lowerpipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0],
                        (upperpipe['x'], upperpipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1],
                        (lowerpipe['x'], lowerpipe['y']))

        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['PLAYER'], (playerx, playery))
        mydigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in mydigits:
            width += GAME_SPRITES['NUMBERS'][digit].get_width()
        xoffset = (SCREENWIDTH - width)/2

        for digit in mydigits:
            SCREEN.blit(GAME_SPRITES['NUMBERS'][digit],
                        (xoffset, SCREENHEIGHT*0.005))
            xoffset += GAME_SPRITES['NUMBERS'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def collide(playerx, playery, upperpipes, lowerpipes):
    if playery > GROUNDY or playery < 0:
        GAME_SOUNDS['hit'].play()
        return True

    for pipe in upperpipes:
        pipeheight = GAME_SPRITES['pipe'][0].get_height()
        if (playery < pipeheight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()

    for pipe in lowerpipes:
        if (playery + GAME_SPRITES['PLAYER'].get_height() > pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()

    return False


def getRandompipe():
    pipeheight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/10
    y2 = offset + random.randrange(0, int(SCREENHEIGHT -
                                   GAME_SPRITES['base'].get_height() - 1.2 * offset))
    pipex = SCREENWIDTH + 10
    y1 = pipeheight + offset - y2
    pipe = [
        {'x': pipex, 'y': -y1},
        {'x': pipex, 'y': y2}
    ]
    return pipe


if __name__ == "__main__":

    pygame.init()  # initialize all pygame modules
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird Game')
    GAME_SPRITES['NUMBERS'] = (

        pygame.image.load('sprites/0.png').convert_alpha(),
        pygame.image.load('sprites/1.png').convert_alpha(),
        pygame.image.load('sprites/2.png').convert_alpha(),
        pygame.image.load('sprites/3.png').convert_alpha(),
        pygame.image.load('sprites/4.png').convert_alpha(),
        pygame.image.load('sprites/5.png').convert_alpha(),
        pygame.image.load('sprites/6.png').convert_alpha(),
        pygame.image.load('sprites/7.png').convert_alpha(),
        pygame.image.load('sprites/8.png').convert_alpha(),
        pygame.image.load('sprites/9.png').convert_alpha(),
    )

    GAME_SPRITES['message'] = pygame.image.load(
        'sprites/message.png').convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load(
        'sprites/base.png').convert_alpha()
    GAME_SPRITES['pipe'] = (pygame.transform.rotate(pygame.image.load('sprites/pipe.png').convert_alpha(), 180),
                            pygame.image.load(
                                'sprites/pipe.png').convert_alpha()
                            )

    # game sounds
    GAME_SOUNDS['die'] = pygame.mixer.Sound('audio/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('audio/swoosh.wav')
    GAME_SOUNDS['wings'] = pygame.mixer.Sound('audio/wings.wav')

    GAME_SPRITES['BACKGROUND'] = pygame.image.load(
        'sprites/background.png').convert()
    GAME_SPRITES['PLAYER'] = pygame.image.load(
        'sprites/bird.png').convert_alpha()

    while True:
        welcomescreen()
        maingame()
