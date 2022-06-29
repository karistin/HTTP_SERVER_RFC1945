from functools import wraps
# 디버깅을 가능하게 해준다. 

def without_wraps(func):
    def __wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return __wrapper

@without_wraps
def my_func_a():
    """Here is my_func_a doc string text."""
    pass

print(my_func_a.__doc__)
print(my_func_a.__name__)


def with_wraps(func):
    @wraps
    def __wrapper(*args, **kwargs):
       return func(*args, **kwargs)
    return __wrapper

@with_wraps
def my_func_b():
    """Here is my_func_b doc string text."""
    pass

print(my_func_b.__doc__)
print(dir(my_func_b))