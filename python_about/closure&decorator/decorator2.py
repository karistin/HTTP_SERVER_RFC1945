from functools import wraps

# def hi_function():
#     print('함수 시작')
#     print('hi')
#     print('함수 끝')

# def hello_function():
#     print('함수 시작')
#     print('hello')
#     print('함수 끝')

def decorator_exam(func):
    @wraps(func)
    def __wrapper(*args, **kwargs):
        print("func start")
        func()
        print("func end")
    return __wrapper

@decorator_exam
def hi_function():
    print("hi")

@decorator_exam
def hello_function():
    print("hello")

# a = hi_function()
# b = hello_function()

class DecoratorExam:
    def __init__(self, func):
        self.func = func
    
    def __call__(self, *args, **kwargs):
        print('func start')
        self.func(*args, **kwargs)
        print('func end ')

@DecoratorExam
def world_function():
    print('world')

# a = world_function()

# https://cjh5414.github.io/python-decorator/

def arg_test(x,y,z):
    @wraps
    def wrap(func):
        @wraps(func)
        def wrap_f(*args, **kwargs):

            result = func(*args, **kwargs)
            return result

        return wrap_f
    return wrap

# def add(x, y):
#     print('add call')
#     return x+y

# v = arg_test(1,2,3)
# x = v(add)
# z = x(1,2)
# print(z)

# @arg_test(1,2,3)
# def add_1(x,y):
#     return x+y

# print('add_1 :', add_1(1,2))

# class decoratorWithArguments(object):
#     def __init__(self, arg1, arg2, arg3):
#         """
#         If there are decorator arguments, the function
#         to be decorated is not passed to the constructor!
#         """
#         print ("Inside __init__()")
#         self.arg1 = arg1
#         self.arg2 = arg2
#         self.arg3 = arg3

#     def __call__(self, f):
#         """
#         If there are decorator arguments, __call__() is only called
#         once, as part of the decoration process! You can only give
#         it a single argument, which is the function object.
#         """
#         print ("Inside __call__()")
#         def wrapped_f(*args):
#             print ("Inside wrapped_f()")
#             print ("Decorator arguments:", self.arg1, self.arg2, self.arg3)
#             f(*args)
#             print ("After f(*args)")
#         return wrapped_f



# @decoratorWithArguments("hello", "world", 42)
# def sayHello(a1, a2, a3, a4):
#     print ('sayHello arguments:', a1, a2, a3, a4)



# print ("After decoration")
# print ("Preparing to call sayHello()")
# sayHello("say", "hello", "argument", "list")
# print ("after first sayHello() call")
# sayHello("a", "different", "set of", "arguments")
# print ("after second sayHello() call")


def route(*args, **kwargs):
    
    print(args, kwargs)

    def wrap(func):

        print(func)

        
        def wrapper(*args, **kwargs):
            
            # print(func.__name__)
            print(args, kwargs)
            
            

            # if args[0] == '/':
            #     self.func1 = func    
            
            # elif args[0] == '/post':
            #     self.func2 = func
            
            # else:
            #     self.func3 = func
        return wrapper
        
    return wrap 

a = route('/')
print(a)