#carGame.py
#

from math import *

from pygame.pixelarray import *

from myPyGameBase import *
from gameController import *
from gameInterface import *

class CarGame:

    def __init__(self, screen, screenSize, sprites):

        carRect = Rect(100, 150, \
                       sprites[4].get_width(), sprites[4].get_height())
        self.car = Car(self, sprites[4], carRect)

        self.gameIf = GameInterface(self) #mostly used by the AiController
        self.controller = AiController(self)
        
        # actions afforded to the player
        self.actionsList = (            \
            "left",     "right",    \
            "acc",      "brake",    \
            "reverse",  "restart",  \
            "endGame" \
            )

        self.actions = dict()
        for action in self.actionsList:
            self.actions.update({action: 0})

        self.running = True
        self.screen = screen
        self.drawOffset = [0, 0]

        self.lvlmap = Map(self, sprites[5])

    def putEvent(self, event):
        self.controller.putEvent(event)
        
    def update(self, dTime, elTime):

        self.controller.update(dTime, elTime)

        self.car.update(dTime, elTime)

        if self.actions["restart"] == 1:
            return 2
        else: return 0

    def draw(self):
        self.lvlmap.draw()
        self.car.draw()
        self.gameIf.draw()

class Car(GameObject):
    
    def __init__(self, host, sprite, rect):

        GameObject.__init__(self, host, sprite, rect, True)
        self.host = host

        self.direction = float(2.0 * pi)
        self.speed = 0.0
        self.vel = Vect2()

        self.enginePower = 50.0
        self.throttle = 1.0
        self.brakingPower = 300.0
        self.braking = 0.0
        self.maxSpeed = 320.0
        
        self.wheelPos = 0.0
        #self.maxWheelAbsPos = pi / 2.0
        
    def update(self, dTime, elTime):

        commonDigit = 4.0
        # turn left
        if self.host.actions["left"] == 1:
            self.wheelPos = 3.0 * pi \
                            * log10(100 + abs(self.speed) ** commonDigit) * dTime
            
        # turn right
        elif self.host.actions["right"] == 1:
            self.wheelPos = -3.0 * pi \
                            * log10(100 + abs(self.speed + 0.1) ** commonDigit) * dTime
        
        # not turning
        else:
            self.wheelPos = 0.0
        
        # accelerate
        if self.host.actions["acc"] == 1:# and self.currentSpeed < self.maxSpeed:
            self.throttle = 1.0
            self.braking = 0.0

        # decelerate
        elif self.host.actions["brake"] == 1:# and self.currentSpeed > -self.maxSpeed / 2:
            self.braking = 1.0
            self.throttle = 0.0

        else:
            self.throttle = 0.0
            self.braking = 0.0

        # reverse
        gear = 1.0 #fwgear
        if self.host.actions["reverse"] == 1:
            gear = -0.5
            
        # loop around rotation-value, no real benefit but lets do it anyway
        while self.direction < -1.0 * pi: self.direction += 2.0 * pi
        while self.direction > 1.0 * pi: self.direction -= 2.0 * pi

        # integrate speed
        self.speed += self.throttle * gear * self.enginePower * dTime
        if self.speed > self.maxSpeed: self.speed = self.maxSpeed
        if self.speed < -1.0 * self.maxSpeed: self.speed = -1.0 * self.maxSpeed
        
        # integrate braking
        brakingEffect = self.braking * self.brakingPower * dTime
        if self.speed > 0.0 + brakingEffect:
            self.speed -= brakingEffect
        if self.speed < 0.0 - brakingEffect:
            self.speed += brakingEffect
        if abs(brakingEffect) > abs(self.speed) \
           and self.braking != 0.0: self.speed = 0.0
        
        # out of bounds
        ooboundsSpeed = 35.0
        emergBrakeAmount = 1.0 * self.brakingPower * dTime
        if self.host.lvlmap.rectCollidingOnMap(self.drawRect):
            if self.speed > ooboundsSpeed + emergBrakeAmount:
                self.speed -= emergBrakeAmount
                if abs(ooboundsSpeed + brakingEffect) > abs(self.speed):
                   self.speed = ooboundsSpeed

            if self.speed < -1.0 * (ooboundsSpeed + emergBrakeAmount):
                self.speed += emergBrakeAmount
                if abs(ooboundsSpeed + brakingEffect) > abs(self.speed):
                   self.speed = -1.0 * ooboundsSpeed

        # update fields/integrate physics
        self.vel = Vect2(1.0, 0.0)
        self.vel.rotate(-1.0 * self.direction)

        self.vel.x = self.vel.x * self.speed * dTime
        self.vel.y = self.vel.y * self.speed * dTime
        
        self.rect.x += self.vel.x
        self.rect.y += self.vel.y

        if self.speed > 20.0 or self.speed < -10.0:
            self.direction += self.wheelPos * .5 * pi * dTime

        self.angle = degrees(self.direction)

class Map(GameObject):
    
    def __init__(self, host, sprite):

        GameObject.__init__(self, host, sprite, Rect(), False)
        self.host = host
    
        mapData = PixelArray(sprite)
        self.bitstring = list()
        
        for pxlarr in mapData:
            for pxl in pxlarr:
                if pxl != 0: self.bitstring.append(0)
                else: self.bitstring.append(1)

        self.dims = [sprite.get_width(), sprite.get_height()]
        self.lvlRect = Rect(0, 0, self.dims[0], self.dims[1])
                    
    def update(self, dTime, elTime):
        pass

    def draw(self):
        GameObject.draw(self)

    def rectCollidingOnMap(self, rect):

        if not self.lvlRect.intersects(rect):
            return True

        #checkThis is list of color-values of lvl-bitmap
        checkThis = self.host.lvlmap.getCollidingPixels(rect)
        for nr in checkThis:
            if nr != 0:
                return True
        return False

    # get part (smaller matrice) of large matrice/2d vector
    # larger matrice is self.bitstring
    def getCollidingPixels(self, collidingRect):

        newbitstring = list()

        offsetX = int(collidingRect.x)
        offsetY = int(collidingRect.y)
        width = int(collidingRect.w)
        height = int(collidingRect.h)
        
        col = 0
        while col < width:
            row = 0
            while row < height:
                ind = (col + offsetX) * self.dims[1] + \
                      (row + offsetY)
                      
                if ind < self.dims[0] * self.dims[1]: 
                    newbitstring.append(self.bitstring[ind])
                row += 1
            col += 1

        return newbitstring



