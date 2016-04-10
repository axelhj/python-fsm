#myPyGameBase.py
#

import copy
from math import *

import pygame

class GameObject:

    def __init__ (self, host, sprite, rect, rotate = False):
        self.host = host
        self.sprite = sprite
        self.drawRect = self.rect = rect
        self.rotate = rotate
        self.angle = 0.0
        
    def move(self, x, y):
        self.rect.x += x
        self.rect.x += y

    def update(self, dTime, elTime):
        pass
    
    def draw(self):
        rect = Rect(self.rect.x - self.host.drawOffset[0], \
                     self.rect.y - self.host.drawOffset[1], \
                     self.sprite.get_width(), \
                     self.sprite.get_height() \
                     )

        if self.rotate == False:
             self.host.screen.blit(self.sprite, rect.asTuple())
        else:
            sprite = pygame.transform.rotate(self.sprite, self.angle)
            rect.w, rect.h = sprite.get_width(), sprite.get_height()
            rect -= Vect2(rect.w / 2.0, rect.h / 2.0)
            self.host.screen.blit(sprite, rect.asTuple())
        self.drawRect = rect

class Dot(GameObject):
    def __init__(self, host, point, color = (255, 0, 0)):

        size = (10, 10)
        
        rect = Rect(point.x, point.y, size[0], size[1])
        rect -= Vect2(size[0] / 2, size[1] / 2)
        
        sprite = pygame.Surface(size)
        pyrect = (int(rect.w), int(rect.h), int(rect.w), int(rect.h))
        
        pyrect = pygame.Rect(0, 0, int(rect.w), int(rect.h))
        pyrect = pygame.draw.rect(sprite, color, pyrect)

        GameObject.__init__(self, host, sprite, rect, False)

    def draw(self):
        rect = Rect(self.rect.x - self.host.drawOffset[0], \
                     self.rect.y - self.host.drawOffset[1], \
                     self.sprite.get_width(), \
                     self.sprite.get_height() \
                     )
        rect -= Vect2(rect.w / 2.0, rect.h / 2.0)
        self.host.screen.blit(self.sprite, rect.asTuple())
        
class Events:
    def __init__(self, host):
        self.host = host

def readFileMatrix(name):
    fdata = open(name, 'r')
    matrix = [ map(int, line.split(' ')) for line in fdata ]
    return matrix

def clamp(max, val):
    return clamp(0, max, val)
 
def clamp(min, max, val = 0):
    if val < min: return min
    if val > max: return max
    else: return val

class Vect2:
    def __init__(self, x = 0.0, y = 0.0):
        self.x = x
        self.y = y

    def copy(self):
        return copy.deepcopy(self)

    def asTuple(self):
        return (self.x, self.y)
    
    def asPoint(self):
        return Point(self.x, self.y)

    def invert(self):
        self.x = -1.0 * self.x
        self.y = -1.0 * self.y
        return self

    def length(self):
        return sqrt(self.x * self.x + self.y * self.y)

    def rotate(self, theta):
        px = self.x
        py = self.y
        ox = 0
        oy = 0
        distance = sqrt(self.x * self.x + self.y * self.y)
        #self.x = distance * cos(theta - atan2(self.y, self.x))
        #self.y = distance * sin(theta - atan2(self.y, self.x))
        self.x = cos(theta) * (px-ox) - sin(theta) * (py-oy) + ox
        self.y = sin(theta) * (px-ox) + cos(theta) * (py-oy) + oy
        return self

    def __add__(self, other):
        return Vect2(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Vect2(self.x - other.x, self.y - other.y)


    def __iadd__(self, other):
        self.x = self.x + other.x
        self.y = self.y + other.y
        return self
    
    def __isub__(self, other):
        self.x = self.x - other.x
        self.y = self.y - other.y
        return self

class Point:
    def __init__(self, x = 0.0, y = 0.0):
        self.x = x
        self.y = y

    def copy(self):
        return copy.deepcopy(self)

    def asTuple(self):
        return [self.x, self.y]

    def asVect2(self):
        return Vect2(self.x, self.y)

    def rotateAbout(self, otherPoint, theta):
        #self -= otherPoint
        px = self.x
        py = self.y
        ox = otherPoint.x
        oy = otherPoint.y
        #distance = sqrt(self.x * self.x + self.y * self.y)
        #self.x = distance * cos(theta - atan2(self.y, self.x))
        #self.y = distance * sin(theta - atan2(self.y, self.x))
        self.x = cos(theta) * (px-ox) - sin(theta) * (py-oy) + ox
        self.y = sin(theta) * (px-ox) + cos(theta) * (py-oy) + oy
        #self += otherPoint
        return self

    def rotate(self, theta):
        px = self.x
        py = self.y
        ox = 0
        oy = 0
        distance = sqrt(self.x * self.x + self.y * self.y)
        #self.x = distance * cos(theta - atan2(self.y, self.x))
        #self.y = distance * sin(theta - atan2(self.y, self.x))
        self.x = cos(theta) * (px-ox) - sin(theta) * (py-oy) + ox
        self.y = sin(theta) * (px-ox) + cos(theta) * (py-oy) + oy
        return self

    def move(self, vect):
        return self + vect
    
    def translate(self, vect):
        return self + vect

    def setPos(self, point):
        self.x = point.x
        self.y = point.y
        
    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)


    def __iadd__(self, other):
        self.x = self.x + other.x
        self.y = self.y + other.y
        return self
    
    def __isub__(self, other):
        self.x = self.x - other.x
        self.y = self.y - other.y
        return self

class Rect(Point):

    def __init__(self, x = 0.0, y = 0.0, w = 10.0, h = 10.0):
        Point.__init__(self, x, y)
        self.w = w
        self.h = h

    def copy(self):
        return copy.deepcopy(self)

    def asTuple(self):
        return [self.x, self.y, self.w, self.h]
    
    def center(self):
        return Point(self.x + self.w / 2.0, \
                self.y + self.h / 2.0)

    def centerOnXY(self):
        self.x -= self.w / 2.0
        self.y -= self.h / 2.0
        return self

    def intersects(self, other):
        return not((self.x >= other.x + other.w) \
             or (self.x + self.w <= other.x) \
             or (self.y >= other.y + other.h) \
             or (self.y + self.h <= other.y))

    def contains(self, other):
        return (( other.x >= self.x \
            and other.y >= self.y \
            and other.x + other.w <= self.x + self.w \
            and other.y + other.h <= self.y + self.h) \
            or (self.x >= other.x \
            and self.y >= other.y \
            and self.x + self.w <= other.x + other.w \
            and self.y + self.h <= other.y + other.h))

    def __add__(self, other):
        return Rect(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Rect(self.x - other.x, self.y - other.y)
