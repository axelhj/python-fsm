#mainPyGame.py
#
import os, sys
import pygame

from myPyGame import TheGame
from carGame import CarGame

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

def gameInstance(screen, size, sprites):
    return CarGame(screen, size, sprites)

def main():
    #init stuff
    pygame.init()

    #size = width, height = 640, 480
    size = width, height = 1024, 768
    white = 255, 255, 255
    black = 0, 0, 0

    info = pygame.display.Info()
    #size = info.current_w, info.current_h
    screen = pygame.display.set_mode(size)#, pygame.FULLSCREEN)

    pygame.display.set_caption('Something, something, something')
    pygame.mouse.set_visible(1)

    #load images
    images = ("", "", "", "", "car.png", "map.png")
    sprites = list()
    for image in images:
        if image == "":
            sprites.append(pygame.image.load("car.png").convert())
        else:
            sprites.append(pygame.image.load(image).convert())

    for ind in range(3):
        rect = sprites[ind].get_rect()
        sprites[ind] = pygame.transform.scale(sprites[ind], (rect.width * 2, \
                                             rect.height * 2))

    #timing-values
    elTicks = pygame.time.get_ticks()
    goalFps = 60.0
    secondsPerFrame = 1.0 / goalFps
    ticksPerFrame = 1000.0 / goalFps
    deltaTicks = ticksPerFrame

    #load the game and run the loop
    game = gameInstance(screen, size, sprites)
    toggleDrawing = True
    while game.running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT or \
               (event.type == pygame.KEYDOWN and \
                event.key == pygame.K_ESCAPE):
                game.running = False;
            else: game.putEvent(event)
            if (event.type == pygame.KEYDOWN and \
                event.key == pygame.K_r):
                game = gameInstance(screen, size, sprites)
            if (event.type == pygame.KEYDOWN and \
                event.key == pygame.K_SPACE):
                 toggleDrawing = not toggleDrawing

        if game.update(secondsPerFrame, elTicks / 1000.0) == 2:
            game = gameInstance(screen, size, sprites)

        if toggleDrawing:
            #screen.fill(black)
            screen.fill(white)

            game.draw()
            pygame.display.flip()

        #deltaTicks = pygame.time.get_ticks() - elTicks
        #elTicks = pygame.time.get_ticks()
        #if (deltaTicks < ticksPerFrame):
        #    pass#pygame.time.wait(int(ticksPerFrame - deltaTicks))

    pygame.quit()

main()

##def load_image(name, colorkey=None):
##    fullname = os.path.join('data', name)
##    try:
##        image = pygame.image.load(fullname)
##    except pygame.error, message:
##        print 'Cannot load image:', name
##        raise SystemExit, message
##    image = image.convert()
##    if colorkey is not None:
##        if colorkey is -1:
##            colorkey = image.get_at((0,0))
##        image.set_colorkey(colorkey, RLEACCEL)
##    return image, image.get_rect()
