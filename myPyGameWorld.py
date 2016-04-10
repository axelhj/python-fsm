#myPyGameWorld.py
#

from myPyGameBase import *

class World:

    
    def __init__(self, host, sprites):

        worldMap = readFileMatrix('level0.txt')
        self.drawRect = [-20, 10, host.screenSize[0], host.screenSize[1]]
        self.tileSize = ( 40, 40 )
        
        self.worldTiles = list()
        self.worldSize = (len(worldMap), len(worldMap[0]))
        
        i = 0
        while i < len(worldMap):
            j = 0
            while j < len(worldMap[0]):
                tType = worldMap[i][j]
                sprite = 0
                if tType == 1: sprite = 1
                rect = Rect(j*self.tileSize[1], i*self.tileSize[0], \
                            self.tileSize[0], self.tileSize[1])
                self.worldTiles.append( \
                    Tile(host, sprites[sprite], rect, tType))
                j += 1
            i += 1

        #self.drawTiles = list()
            
    def update(self, dTime, elTime):
        pass

    def draw(self):
        tileList = self.populateTileList(self.drawRect)
        for tile in tileList:
            tile.draw()

    def populateTileList(self, partRect):
        tileList = list()

        horFirstIndex = partRect[0] / self.tileSize[0]
        horLastIndex = (partRect[2] / self.tileSize[0]) + horFirstIndex + 1

        vertFirstIndex = partRect[1] / self.tileSize[1]
        vertLastIndex = (partRect[3] / self.tileSize[1]) + vertFirstIndex + 1
        
        col = horFirstIndex
        while col <= horLastIndex:
            row = vertFirstIndex    
            while row <= vertLastIndex:
                if col >= 0 and row >= 0:
                    calcInd = row * self.worldSize[1] + col
                    #print calcInd
                    if calcInd < self.worldSize[0] * self.worldSize[1]:
                        tileList.append(self.worldTiles[calcInd])
                row += 1
            col += 1
        return tileList

class Tile(GameObject):

    def __init__(self, host, sprite, rect, tType):
        GameObject.__init__(self, host, sprite, rect)
        self.tType = tType

    def draw(self):
        if self.rect.x >= 0 and self.rect.y >= 0:
            GameObject.draw(self)

        

