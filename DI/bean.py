from typing import get_type_hints

providers = {}


def bean(cls):
    obj = cls()
    providers[cls] = obj
    return cls


def get_bean(cls):
    if get_type_hints(providers[cls]):
        for key, value in get_type_hints(providers[cls]).items():  
            for provider in providers.keys():
                base = []
                while True:
                    if type(provider) == type(object):
                        break
                    base.append(provider)
                    provider = provider.__base__
                for tem in base:
                    if value == tem.__base__:
                        setattr(providers[cls], key, providers[tem])                      
    return providers[cls]


