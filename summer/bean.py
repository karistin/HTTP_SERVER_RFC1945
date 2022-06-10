from ball  import ball
import inspect
from functools import wraps

bean = {}


def injection(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        bean[ball] = func()
        print(bean)
        return func(*args, **kwargs) 

    return wrapper