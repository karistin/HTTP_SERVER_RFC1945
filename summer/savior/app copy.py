from abc import *
from functools import wraps
import inspect

providers = {}

def bean(func):
    
    providers[func.__bases__[0]] = func
    
    def inject(*args, **kwargs):

        # __annotations__

        for provider in providers.keys():
            if func.__annotations__['ball'] == provider:
                func.__annotations__['ball'] = providers[provider]
        

        return func(*args, **kwargs)

    return inject

class Ball(metaclass = ABCMeta):
    @abstractmethod
    def get(self):
        pass
@bean
class adidasball(Ball):
    def get(self):
        return 'adidasball'

# @bean
class nikeball(Ball):
    def get(self):
        return 'nikeball'

@bean
class Soccerplayer:
    ball: Ball

def get_bean(cls):
    # print(cls.__annotations__)
    return cls.__annotations__['ball']
    

if __name__ == "__main__":
    print(providers)
    # test = Soccerplayer()
    # print(test.ball.get())
    
    # test = soccerplayer() 
    # print(test.ball.get())
    
    print(get_bean(Soccerplayer()).get(None))
    # get_bean(Soccerplayer).ball.get()
    
