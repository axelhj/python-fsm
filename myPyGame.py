#myPyGame.py
#

from myPyGameWorld import World
from myPyGameBase import *
from myPyGameChar import Character
from myPyGameItems import Items
from myPyGameEnem import Enemies

class TheGame:

    def __init__(self, screen, screenSize, sprites):

        self.screen = screen
        self.screenSize = screenSize
        self.drawOffset = [0, 0]

        playerSprite = sprites[3]
        playerRect = playerSprite.get_rect()
        playerStartPos = (100.0, 100.0)
        playerRect = Rect(playerStartPos[0], playerStartPos[1], \
                          playerRect.w, playerRect.h)
        
        self.objs = { "enem": Enemies(self, sprites[3]), \
                      "world": World(self, sprites), \
                      "player": Character(self, playerSprite, playerRect), \
                      "items": Items(self, sprites[2])}
        
        self.keys = [0, 0, 0, 0, 0]
        self.running = True

    def update(self, dTime, elTime):

        dTime *= 1 #scale the time.. :-)
        
        for key, obj in self.objs.iteritems(): obj.update(dTime, elTime)

        self.objs["player"].setAcc((self.keys[0], self.keys[1], self.keys[4]))
        self.objs["player"].collideEntities(self.objs["world"])
        self.objs["items"].check(self.objs["player"].rect)

    def setScreenPos(self):
        #manage camera/drawing-position
        playerPos = [self.objs["player"].rect.x, self.objs["player"].rect.y]
        playerPos[0] = playerPos[0] - self.screenSize[0] / 2
        playerPos[1] = playerPos[1] - self.screenSize[1] / 4 * 3
        for ind, nr in enumerate(playerPos): playerPos[ind] = int(nr)
        self.objs["world"].drawRect[:2] = playerPos
        self.drawPos = playerPos

    def draw(self):
        prect = self.objs["player"].rect
        self.drawOffset = \
                [-self.screenSize[0] / 2 + prect.x, \
                 -self.screenSize[1] / 4 * 3 + prect.y]
        self.setScreenPos()

        for key, obj in self.objs.iteritems(): obj.draw()
        
    def setKeys(self, keys):
        self.keys = keys
                
class Ball(GameObject):

    def __init__(self, screen, spriteImage,  screenM, pos):

        GameObject.__init__(self, screen, spriteImage, screenM, pos)
        self.speed = [1, 1]

    def update(self):

        if self.rect.left < 0 or self.rect.right > self.screenMetr[0]:
            self.speed[0] = -self.speed[0]
        if self.rect.top < 0 or self.rect.bottom > self.screenMetr[1]:
            self.speed[1] = -self.speed[1]
        self.move(self.speed[0], self.speed[1])

