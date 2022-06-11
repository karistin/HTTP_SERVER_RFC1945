from typing import get_type_hints


providers = {}

# def bean(func):
    
#     providers[func.__bases__[0]] = func
    
#     def inject(*args, **kwargs):

#         # __annotations__
#         # print(providers)

#         for provider in providers.keys():
#             if func.__annotations__['ball'] == provider:
#                 func.__annotations__['ball'] = providers[provider]
        

#         return func(*args, **kwargs)

    # return inject

def bean(cls):
    obj = cls()
    # 오브젝트 로 만들고 같은 속성이 있다면 연결하시오로 만들어야된다!!!!
    provider[cls] = obj
    get_type_hints(obj)
    return cls

def get_bean(cls):
    # print(cls.__annotations__)
    return cls.__annotations__['ball']
