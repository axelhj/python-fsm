#myPyGameEnem.py
#

from myPyGameBase import *

class Enemies:

    def __init__(self, host, sprite):
        self.enems = list()
        self.enems.append(Enem(host, sprite, Rect(250, 300, 40, 40)))

    def update(self, dTime, elTime):
        for enem in self.enems: enem.update(dTime, elTime)


    def draw(self):
        for enem in self.enems: enem.draw()
        
class Enem(GameObject):

    def __init__(self, host, sprite, rect):
        GameObject.__init__(self, host, sprite, rect)
        self.vel = [0.0, 0.0]
        self.speed = 35.0
        self.bounds = [200, 800]

        self.vel[0] = float(self.speed)
        
    def update(self, dTime, elTime):

        self.rect.x += (self.vel[0] * dTime)
        self.rect.y += (self.vel[1] * dTime)

        if self.rect.x > self.bounds[1]: self.vel[0] = -self.speed
        if self.rect.x < self.bounds[0]: self.vel[0] = self.speed
        
    def draw(self):
        GameObject.draw(self)

