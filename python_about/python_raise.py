# https://blockdmask.tistory.com/538


# 그냥  raise
from logging import exception


a = int(input("1~5 까지 숫자 입력: "))

if a<1 or a>5:
    raise

print(f'입력한 a: {a}입니다.')


# 1-2) raise + 예외처리 이름
a = int(input("1~5 까지 숫자 입력: "))

if a<1 or a>5:
    raise ValueError

print(f'입력한 a: {a}입니다.')

# 1-3) raise + 메시지
a = int(input("1~5 까지 숫자 입력: "))

if a<1 or a>5:
    raise Exception("error")

print(f'입력한 a: {a}입니다.')

# 2) 파이썬 예외처리 try + raise + except

try:
    a = int(input("1~5 까지 숫자 입력: "))

    if a<1 or a>5:
        raise 

    print(f'입력한 a: {a}입니다.')
except:
    print("1~5 입력하라고")