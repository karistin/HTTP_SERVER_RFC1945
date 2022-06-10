import abc


class ball:
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def get(self):
        pass
