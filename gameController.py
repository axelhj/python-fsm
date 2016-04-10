#gameController.py
#

import pygame
from gameInterface import *
from controlStates import *

class BaseController:

    def __init__(self, gameInstance):
        self.gameInterface = gameInstance.gameIf

        #print gameInstance.actionsStatus

    def putEvent(self, event):
        pass
        
    def update(self, dTime, elTime):
        pass

class AiController(BaseController):

    def __init__(self, gameInstance):
        BaseController.__init__(self, gameInstance)

        statesDict = dict()
        statesDict.update({ \
##            "left":     StateLeft(self.gameInterface, statesDict), \
##            "right":    StateRight(self.gameInterface, statesDict), \
            "steer":    StateSteer(self.gameInterface, statesDict), \
            "acc":      StateAcc(self.gameInterface, statesDict), \
            "brake":    StateBrake(self.gameInterface, statesDict), \
            "reverse":  StateReverse(self.gameInterface, statesDict), \
            "idle":     StateIdle(self.gameInterface, statesDict) \
            })
        self.currentState = statesDict["acc"]
        self.statesDict = statesDict
        
    def update(self, dTime, elTime):
        # i want to go faster/slower/left/right
        # is collission ahead indicating faster/slower going,
        # turning left or right most favorable
        #  - handled by Finite state machine

        for key in self.gameInterface.gameInstance.actions:
            if self.gameInterface.gameInstance.actions[key] != 0:
                self.gameInterface.gameInstance.actions[key] = 0
        self.currentState.Update(dTime, elTime)
        self.currentState = self.statesDict[self.currentState.Exit()]
        #print self.currentState.state

class KeybController(BaseController):

    def __init__(self, gameInstance):
        BaseController.__init__(self, gameInstance)

        keys = ( \
            pygame.K_LEFT, #left
            pygame.K_RIGHT,#right
            pygame.K_UP,   #acc
            pygame.K_DOWN, #brake
            pygame.K_LCTRL,#reverse
            pygame.K_r,    #restart
            #pygame.K_ESC,  #endGame
            pygame.K_RCTRL,
            #pygame.K_SPACE,
            \
            )

        self.keyToAction = dict()
        for key, action in zip(keys, self.gameInterface.gameInstance.actionsList):
            self.keyToAction.update({key: action})
        self.keyToAction[pygame.K_RCTRL] = self.keyToAction[pygame.K_LCTRL]

    def putEvent(self, event):
        
        # keys down
        if event.type == pygame.KEYDOWN \
           and event.key in self.keyToAction:
                self.gameInterface.activateGameAction(self.keyToAction[event.key])
        # keys up
        elif event.type == pygame.KEYUP \
             and event.key in self.keyToAction:
                self.gameInterface.deactivateGameAction(self.keyToAction[event.key])

    def update(self, dTime, elTime):
        pass


                


