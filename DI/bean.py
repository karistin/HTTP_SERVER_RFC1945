from typing import get_type_hints

providers = {}

temp = []

def bean(cls):
    obj = cls()
    # 오브젝트 로 만들고 같은 속성이 있다면 연결하시오로 만들어야된다!!!!
    
    providers[cls] = obj
    
    # print(providers)
    

    def wrapper(*args, **kwargs):

        hints = get_type_hints(cls)
        
        if len(hints.values()) > 0:
            for hint in hints.values():
                for provider in providers.keys():                    
                    # baes는 tuple , interface는 하나만 존재한다 가정
                    if hint == provider.__bases__[0]:
                        temp.append(provider)
        return cls(*args, **kwargs)

    return wrapper

def get_bean(cls):

    test = cls()
    test.ball = temp[0]

    return test
