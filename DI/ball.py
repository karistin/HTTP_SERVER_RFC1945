from abc import *

class Ball(metaclass = ABCMeta):
    @abstractmethod
    def get():
        pass