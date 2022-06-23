# Where is Hi ?
# def outer_func():
#     message = "Hi"

#     def inner_func():
#         print(message)
    
#     return inner_func

# func = outer_func()

# print(func) 
# Hi 변수는 outer func에 저장되어 있지만 이를  inner_func의 closure 에도 저장이 되어 있다. 

# print()

# print(dir(func))

# print()

# print(type(func.__closure__))

# print()

# print(func.__closure__)

# print()

# print(func.__closure__[0])

# print()

# print(dir(func.__closure__[0]))

# print()

# print(func.__closure__[0].cell_contents)

# <function outer_func.<locals>.inner_func at 0x7f4f68df9c10>

# ['__annotations__', '__call__', '__class__', '__closure__', '__code__', '__defaults__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__get__', '__getattribute__', '__globals__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__kwdefaults__', '__le__', '__lt__', '__module__', '__name__', '__ne__', '__new__', '__qualname__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__']

# <class 'tuple'>

# (<cell at 0x7f4f68e8dd60: str object at 0x7f4f68e00730>,)

# <cell at 0x7f4f68e8dd60: str object at 0x7f4f68e00730>

# ['__class__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'cell_contents']

# Hi

def outer_func(tag):
    tag = tag
    
    def inner_func(txt):
        text = txt
        print('<{0}>{1}<{0}>'.format(tag, text))
    
    return inner_func

h1_func = outer_func('h1')
p_func = outer_func('p')

h1_func('h1 테그의 안입니다. ')
p_func('p 태그의 안입니다. ')