from abc import *
from functools import wraps
import inspect

class ball(metaclass = ABCMeta):

    @abstractmethod
    def get(self):
        pass

class adidasball(ball):

    def get(self):
        return 'adidasball'

class nikeball(ball):

    def get(self):
        return 'nikeball'


providers = {
    # ball : adidasball
    ball : nikeball
}


def inject(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        annotations = inspect.getfullargspec(func).annotations


        for k, v in annotations.items(): 
            if v in providers:
                kwargs[k] = providers[v]()
        
        print(annotations.items())
        return func(*args, **kwargs)
    return wrapper


class soccerplayer:
    @inject
    def __init__(self, ball : ball):
        self.ball = ball
    

if __name__ == "__main__":
    test = soccerplayer() 
    print(test.ball.get())