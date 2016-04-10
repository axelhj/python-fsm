#controlStates.py
#

from myPyGameBase import *

class State:
    def __init__(self, gameIf, statesDict):
        self.gameIf = gameIf #game interface for allowing ai control
        self.statesDict = statesDict
        self.state = "base - nullstate"

        self.angle = pi / 2
        self.centerDist = 125.0
        self.dist = 35.0
        
    def Enter(self):
        pass #not used

    def Exit(self):
        return "acc"

    def Update(self, dTime, elTime):
        self.gameIf.activateGameAction(self.state)

class StateSteer(State):
    def __init__(self, gameIf, statesDict):
        State.__init__(self, gameIf, statesDict)
        self.state = "steer"
        
    def Update(self, dTime, elTime):
        state = 0
        left, right = self.gameIf.getLeftView(self.dist, self.angle), \
                      self.gameIf.getRightView(self.dist, self.angle)
        if not left and not right: return
        if not left:
            state = "left"
        elif not right:
            state = "right"
        if state != 0: self.gameIf.activateGameAction(state)
        return
        
    def Exit(self):
        if not (self.gameIf.getLeftView(self.dist, self.angle) and \
            self.gameIf.getRightView(self.dist, self.angle)) and not \
            self.gameIf.getCenterView(self.centerDist):
            return "acc"
        if (self.gameIf.getLeftView(self.dist, self.angle) and \
            self.gameIf.getRightView(self.dist, self.angle)) and \
            self.gameIf.hitTerrain() and \
           self.gameIf.getCenterView(self.centerDist):
            return "reverse"
        if (not (self.gameIf.getLeftView(self.dist, self.angle) and \
            self.gameIf.getRightView(self.dist, self.angle)) and \
            self.gameIf.hitTerrain() and \
           self.gameIf.getCenterView(self.centerDist)):
            return "acc"
        return self.state

class StateAcc(State):
    def __init__(self, gameIf, statesDict):
        State.__init__(self, gameIf, statesDict)
        self.state = "acc"

    def Exit(self):
##        if self.gameIf.getCenterView(self.centerDist):
##            return "steer"
##        if not (self.gameIf.getLeftView(self.dist, self.angle) and \
##            self.gameIf.getRightView(self.dist, self.angle)) and not \
        if not self.gameIf.hitTerrain() and \
           self.gameIf.getCenterView(self.centerDist) and \
           self.gameIf.gameInstance.car.speed > 15.0:
            return "brake"
        if (self.gameIf.getLeftView(self.dist, self.angle) or \
            self.gameIf.getRightView(self.dist, self.angle) or \
            self.gameIf.hitTerrain()) and \
            self.gameIf.getCenterView(self.centerDist):
            return "steer"
        return "acc"

class StateReverse(State):
    def __init__(self, gameIf, statesDict):
        State.__init__(self, gameIf, statesDict)
        self.state = "reverse"

    def Update(self, dTime, elTime):
        if self.gameIf.gameInstance.car.speed > 5.0:
            self.gameIf.activateGameAction("brake")
        else:
            self.gameIf.activateGameAction(self.state)
            self.gameIf.activateGameAction("acc")
        
    def Exit(self):
        if self.gameIf.getCenterView(self.centerDist):
            return "steer"
        if not self.gameIf.hitTerrain() or not \
           (self.gameIf.getLeftView(self.dist, self.angle) and \
            self.gameIf.getRightView(self.dist, self.angle)):
            return "acc"
        return self.state

class StateBrake(State):
    def __init__(self, gameIf, statesDict):
        State.__init__(self, gameIf, statesDict)
        self.state = "brake"

    def Exit(self):
        if self.gameIf.hitTerrain() and \
           self.gameIf.getCenterView(self.centerDist):
            return "reverse"
        if not self.gameIf.hitTerrain() and \
           self.gameIf.getCenterView(self.centerDist):
            return "steer"
        if self.gameIf.hitTerrain()  and not \
           self.gameIf.getCenterView(self.centerDist):
            return "acc"
        if self.gameIf.gameInstance.car.speed < 15: return "steer"
        return self.state
        
class StateIdle(State):
    def __init__(self, gameIf, statesDict):
        State.__init__(self, gameIf, statesDict)
        self.state = "idle"

    def Update(self, dTime, elTime):
            pass
    
    def Exit(self):
        if not (self.gameIf.getCenterView(self.centerDist) and \
                self.gameIf.getRightView(self.dist, self.angle) and \
                self.gameIf.getLeftView(self.dist, self.angle)): return "acc"
        #if self.
        return "right"
