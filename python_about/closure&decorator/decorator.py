
# method decorator

# def decorator_function(original_function):
#     def wrapper_function(*args, **kwargs):
#         print('{} 함수가 호출되기전 입니다.'.format(original_function.__name__))
#         return original_function(*args, **kwargs)
#     return wrapper_function

# @decorator_function
# def display_1():
#     print('display_1 함수가 실행됐습니다.')

# @decorator_function
# def display_info(name, age):
#     print('display_info({}, {}) 함수가 실행됐습니다.'.format(name, age))

# # display_1 = decorator_function(display_1)
# # display_2 = decorator_function(display_2)

# display_1()
# print()
# display_info('John', 25)


# class decorator

class DecoratorClass:
    def __init__(self, original_function):
        self.original_function = original_function
    
    def __call__(self, *args, **kwargs):
        print('{} 함수가 호출되기전 입니다.'.format(self.original_function.__name__))
        return self.original_function(*args, **kwargs)
    
@DecoratorClass
def display():
    print('display 함수가 실핼됐습니다.')

@DecoratorClass
def display_info(name, age):
    print('display_info({}, {})'.format(name, age))

# display()
# print()
# display_info('John', 25)





def templated(template=None):
    print('before templated')
    
    def decorator(func):
        
        print('before decorator')
        
        def decorated_function(*args, **kwargs):
            
            print('decorated_function')
            
            print(template)
            
            template_name = template
            
            ctx = func(*args, **kwargs)
            
            return template_name
        
        return decorated_function
        
        print('after decorator')
    
    return decorator
    
    print('after templated')

@templated('/')
def index(x, y):
    print(x, y)
    pass

print('함수 선언')
print(index(1, 2))