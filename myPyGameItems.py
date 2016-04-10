#myPyGameItems.py
#

from myPyGameBase import *

class Items:

    def __init__(self, host, sprite, ):

        items = readFileMatrix('items0.txt')
        self.items = list()
        
        for row in items:    
            rect = Rect(row[0], row[1], row[2], row[3])
            self.items.append(Item(host, sprite, rect))

    def check(self, plRect):
        i = 0
        while i < len(self.items):
            if self.items[i].rect.intersects(plRect):
                del self.items[i]
            i += 1

    def update(self, dTime, elTime):
        pass
    
    def draw(self):
        for item in self.items:
            item.draw()

class Item(GameObject):

    def __init__(self, host, sprite, rect):
        GameObject.__init__(self, host, sprite, rect)
        self.type = 0

    
