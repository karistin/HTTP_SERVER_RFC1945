# with <expression> as <variable>:
#     <block>


# with open('textfile.txt', 'r') as file:
#     contents = file.read()

# __enter__ 와 __exit__ 메소드 실행 

# Python with절 문법의 이해
# 자원을 획득하고, 사용하고, 반납할때 주로 사용한다.

# 예를들어 파일을 여는 경우, 다른 프로세스를 위해 사용한 뒤에 닫아주어야 한다.

# 또는 DB 세션을 사용하는 경우, 다른 프로세스를 위해 반납해야 한다.

# try / except / finally 구문을 통해 이와같은 구현이 가능하긴 하다.

# 하지만 이러한 방법 역시 예외가 발생하는 케이스 및 탈출 조건을 만족하는 케이스에 대해서 리소스를 정리하는 코드가 중복으로 작성된다.

# 파이썬의 컨텍스트 매니저는 이러한 리소스를 with문법을 통해 with 절 내에서만 액세스를 가능하게 하고, 블록을 나가는 경우 어떤 이유든간에 리소스를 해제하게 된다.

# 다음과 같은 구조로 사용한다.



# 출처: https://projooni.tistory.com/entry/Python-with절-문법의-이해 [Lithium Flower]


# Python의 with문에 대해서 알아보겠습니다.

# ​

# 자원을 획득하고 사용 후 반납해야 하는 경우 주로 사용합니다.

# 1) 자원을 획득한다

# 2) 자원을 사용한다

# 3) 자원을 반납한다

# ​

# 예를들어 

# 파일을 열고 사용했다면 다른 프로세스를 위해 닫고 반납해야 합니다.

# 데이터베이스 세션을 얻어 사용했다면 다른 프로세스를 위해 반납해야 합니다.

# 자원은 한정되어 있기 때문에 적절히 획득과 반납해야 합니다.


# https://m.blog.naver.com/PostView.naver?isHttpsRedirect=true&blogId=wideeyed&logNo=221653260516

class Hello:
    def __enter__(self):
        # 사용할 자원을 가져오거나 만든다.
        print("enter..")
        return self
    
    def sayHello(self, name):
        print('hello ' + name)
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print('exit...')

with Hello() as h:
    h.sayHello('obama')
    h.sayHello('trump')