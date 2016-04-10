#gameInterface.py
#

from carGame import *
from myPyGameBase import *

class GameInterface:

    def __init__(self, gameInstance):
        
        self.gameInstance = gameInstance
        self.dots = list()

    def activateGameAction(self, actionName):
        self.gameInstance.actions[actionName] = 1
        
    def deactivateGameAction(self, actionName):
        self.gameInstance.actions[actionName] = 0

    def getAheadView(self, dist, angle = 0.0):

        game = self.gameInstance
        
        dirRadians = game.car.direction
        checkPoint = Point(dist, 0.0)
        checkPoint.rotateAbout(Point(0, 0), -1.0 * (dirRadians + angle))
        collissionRect = game.car.rect.copy()
        collissionRect += checkPoint
        self.dots.append(Dot(self.gameInstance, collissionRect.center()))
        result = game.lvlmap.rectCollidingOnMap(collissionRect)
        return result

    def getCenterView(self, dist):
        return self.getAheadView(dist)

    def getLeftView(self, dist, angle):
        return self.getAheadView(dist, angle)

    def getRightView(self, dist, angle):
        return self.getAheadView(dist, -1.0 * angle)

    def hitTerrain(self):
        return self.gameInstance.lvlmap.rectCollidingOnMap( \
            self.gameInstance.car.rect)

    def draw(self):
        for dot in self.dots:
            dot.draw()

        self.dots = list()
