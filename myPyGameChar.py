#myPyGameChar.py
#

from myPyGameBase import *

class Character(GameObject):

    def __init__(self, host, sprite, rect):
        GameObject.__init__(self, host, sprite, rect)
        
        self.vel = [0.0, 0.0]
        self.acc = [0.0, 0.0]
        self.speed = 20
        self.turnSpeed = 60
        self.maxSpeed = 400
        self.retardSpeed = 12
        
        self.noColls = False
        
        self.jumpAllowed = True
        self.jump = True
        
        self.allowedJumptime = 0.20
        self.jumpTime = 0.0
        self.jumpvel = -370.0
        self.continuedJumpvel = -28
        
        self.gravity = 26.0

    def update(self, dTime, elTime):

        if self.vel[0] < 0: #negative
            if self.vel[0] < -self.maxSpeed:
                self.vel[0] = -self.maxSpeed
            else: self.vel[0] -= -self.retardSpeed
            
        if self.vel[0] > 0: #positive
            if self.vel[0] > self.maxSpeed:
                self.vel[0] = self.maxSpeed
            else: self.vel[0] -= self.retardSpeed

        if abs(self.vel[0]) < 15: self.vel[0] *= 0.8
        if abs(self.vel[0]) < 2: self.vel[0] = 0

        if self.jumpTime > 0: self.jumpTime -= dTime
        
        if self.noColls: self.jump = True

        self.vel[0] += self.acc[0]
        self.vel[1] += self.acc[1]
        self.vel[1] += self.gravity
        self.acc = [0, 0]
        
        self.rect.x += (self.vel[0] * dTime)
        self.rect.y += (self.vel[1] * dTime)
        
    def draw(self):
        GameObject.draw(self)

    def setAcc(self, acc):
        if acc[0] == 1:
            if self.vel[0] > 0: self.acc[0] = -self.turnSpeed
            else: self.acc[0] = -self.speed
        if acc[1] == 1:
            if self.vel[0] < 0: self.acc[0] = self.turnSpeed
            else: self.acc[0] = self.speed
            
        if acc[2] == 0: #not jumping
            if not self.jump and not self.noColls \
               and not self.jumpAllowed:
                self.jumpAllowed = True

        if acc[2] == 1: #jumping
            if self.jump and self.jumpTime > 0:
                self.acc[1] += self.continuedJumpvel
            if not self.jump and self.jumpAllowed:
                self.jump = True
                self.jumpAllowed = False
                self.jumpTime = self.allowedJumptime
                self.acc[1] += self.jumpvel

    def collideEntities(self, world):
        self.noColls = True

        checkRect = (int(self.rect.x - self.rect.w * 2), \
                     int(self.rect.y - self.rect.h * 2), \
                     self.rect.w * 5, self.rect.h * 5)
        checkTiles = world.populateTileList(checkRect)
        
        for tile in checkTiles:
            if tile.rect.intersects(self.rect) and tile.tType == 1:

                self.noColls = False                
                #player not over tile, so under
                if not self.rect.y < tile.rect.y:

                    #player left of tile
                    if self.rect.x < tile.rect.x: 
                        self.rect.x = tile.rect.x - self.rect.w
                        self.vel[0] = 0

                    #player right of tile
                    if self.rect.x + self.rect.w > tile.rect.x + tile.rect.w:
                        self.rect.x = tile.rect.x + tile.rect.w
                        self.vel[0] = 0

                #player over tile
                if self.rect.y < tile.rect.y:
                    self.rect.y = tile.rect.y - self.rect.h
                    self.vel[1] = 0
                    self.jump = False
                    
                #player under tile
                if self.rect.y + self.rect.h > tile.rect.y + tile.rect.h + 1:
                    self.rect.y = tile.rect.y + tile.rect.h
                    self.vel[1] = 0
                    
class Bullet(GameObject):

    def __init__(self, host, sprite, rect, speed):
        GameObject.__init__(self, host, sprite, rect)
        self.vel = speed

    def update(self, dTime, elTime):
        for ind, val in enumerate(self.vel):
            self.rect[ind] += val
        
