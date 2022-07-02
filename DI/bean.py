from typing import get_type_hints

providers = {}

# 모든 해당 클래스의 맴버 (변수, 클래스 타입) 저장 
get_type_value ={}

# 모든 class 저장
get_base = []

def bean(cls):
    obj = cls()
    providers[cls] = obj
    return cls


def get_bean(cls):
    if get_type_value[cls]:
        for get in get_type_value[cls]:
            for key, value in get.items():
                for base in get_base:
                    if value == base.__base__:
                        setattr(providers[cls], key, providers[base])
                        break                            
    return providers[cls]


def initbean():
    for provider in providers.keys():
        get_type_value[provider] = [get_type_hints(provider)]
        while True:
            if type(provider) == type(object):
                break
            if provider in get_base:
                break
            get_base.append(provider)
            provider = provider.__base__

    