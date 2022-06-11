import abc
import inspect
from functools import wraps


class Repo:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get(self):
        pass

class MySQLRepo(Repo):
    def __init__(self):
        self.sql = "mysql"

    def get(self):
        return ('MySQLRepo')

providers = {
    Repo : MySQLRepo,
}

def inject(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        annotations = inspect.getfullargspec(func).annotations

        for k, v in annotations.items(): 
            if v in providers:
                print(providers[v]())
                kwargs[k] = providers[v]()
        
        return func(*args, **kwargs)
    
    return wrapper


class Usecase:
    @inject
    def __init__(self, repo:Repo):
        print(repo)
        self.repo = repo
class Book:
    ksj : int = 123

if __name__ == '__main__':
    usecase = Usecase()

    print(usecase.repo.get())
    print(usecase.repo.sql)

    print(Book.ksj)
# https://www.hides.kr/1053