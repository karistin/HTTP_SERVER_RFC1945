class Repo:
    def get(self):
        return "Repo"

class Usecase:
    def __init__(self):
        self.repo = Repo()

if __name__ == "__main__":
    a = Usecase()
    print(a.repo.get())