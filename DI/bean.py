from typing import get_type_hints

providers = {}

temp = []


def bean(cls):
    obj = cls()
    # 오브젝트 로 만들고 같은 속성이 있다면 연결하시오로 만들어야된다!!!!
    providers[cls] = obj
    return cls


def get_bean(cls):
    return providers[cls]


def init_bean():

    base = {}
    type_hint = {}

    # base dic 과 type_hint dic 생성
    for provider in providers.keys():
        base[provider] = provider.__base__

        if len(list(get_type_hints(provider).values())) == 0:
            pass
        else:
            for val in list(get_type_hints(provider).values()):
                type_hint[provider] = val
    
    for hint_key, hint_value in type_hint.items():
        di_val = [(hint_key, base_key, base_value) for base_key, base_value in base.items() if base_value == hint_value]
        # dic_val (인잭션 받는 클래스 , 인잭션 주는 클래스 , 인잭션 값 )

    # https://technote.kr/248
    print(di_val)
    for i in range(0, len(di_val)):
        (providers.get(di_val[i][0])).ball = providers.get(di_val[i][1])


