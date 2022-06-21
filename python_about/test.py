# from abc import *

# class StudentBase(metaclass = ABCMeta):

#     @abstractmethod
#     def study(self):
#         pass

#     @abstractmethod
#     def go_to_school(self):
#         pass


# class Student():

#     def __init__(self):
#         self.StudentBase = StudentBase

#     def study(self):
#         print('study')


# james = Student()

# james.study()

# james.StudentBase.go_to_school(james)


# class a():

#     def test(self):
#         a = 3
#         self.test2(a)
#         return a

#     def test2(self, a):
#         a += 3

# call = a()

# print(call.test())

from threading import Thread
import threading
from time import sleep

# class a(threading.Thread):

#     def __init__(self) -> None:
#         threading.Thread.__init__(self)
#         self.var = 3 
        
#     def run(self):
#         self.var +=3
#         print(self.var)
#         sleep(0.5)

# t1 = a()
# t2 = a()
# t1.start()
# t2.start()

# class a():


#     def __init__(self) -> None:
#         self.var = 3

#     def run(self):
#         while(1):
#             self.var += 3 
#             print(f'{threading.get_native_id()} : {self.var}')
#             sleep(0.5)
    
#     def cli(self):
#         t1 = threading.Thread(target=self.run)
#         t2 = threading.Thread(target=self.run)
#         t1.start()
#         t2.start()


# a().cli()


import base64
a = {
    'id' : "ksj",
    'password' : '1109'
}

string = 'ksj:1109'
string_encode = string.encode('ascii')
print(base64.b64encode(string_encode))

bs64 = b'a3NqOjExMDk='
print(base64.b64decode(bs64))
# https://webisfree.com/2020-11-07/python-base64-%EC%9D%B8%EC%BD%94%EB%94%A9-%EB%94%94%EC%BD%94%EB%94%A9-%EB%B3%80%ED%99%98-%EB%B0%A9%EB%B2%95