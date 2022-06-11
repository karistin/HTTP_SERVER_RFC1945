from abc import *

class StudentBase(metaclass = ABCMeta):

    @abstractmethod
    def study(self):
        pass

    @abstractmethod
    def go_to_school(self):
        pass


class Student():

    def __init__(self):
        self.StudentBase = StudentBase

    def study(self):
        print('study')


james = Student()

james.study()

james.StudentBase.go_to_school(james)