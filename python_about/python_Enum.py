from enum import Enum, auto
# https://docs.python.org/ko/3/library/enum.html

class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3
    WHITE = auto()

print(repr(Color.RED))
print(repr(Color.WHITE))
# https://shoark7.github.io/programming/python/difference-between-__repr__-vs-__str__

print(Color.RED.value)
# 멤버 값은 아무것이나 될 수 있습니다: int, str 등. 정확한 값이 중요하지 않다면,
# auto 인스턴스를 사용할 수 있으며 적절한 값이 선택됩니다. auto를 다른 값과 혼합 할 경우 주의를 기울여야 합니다. 

# 참고 명명법
# Color 클래스는 열거형(enumeration) (또는 enum) 입니다.

# Color.RED, Color.GREEN 등의 어트리뷰트는 열거형 멤버(enumeration members)(또는 enum members)이며 기능상 상수입니다.

# 열거형 멤버에는 이름(names)과 값(values)이 있습니다 (Color.RED의 이름은 RED, Color.BLUE의 값은 3, 등)
