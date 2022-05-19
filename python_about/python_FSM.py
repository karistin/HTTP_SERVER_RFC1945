from random import randint
from time import _ClockInfo

#======================================================
State = type("State", (object,), {})

class LightOn(State):
    def Execute(self):
        print("Light is On!")
    
class LightOff(State):
    def Execute(self):
        print("Light is Off!")


#======================================================


class Transistion(object):
    def __init__(self, toState):
        self.toState = toState
    
    def Excute(self):
        print("Transitioning.....")

#======================================================

class SimpleFSM(object):
    def __init__(self, char):
        self.char = char
        self.states = {}
        self.transitions = {}
        self.curState = None
        self.trans = None

    def SetState(self, stateName):
        self.curState = self.states[stateName]