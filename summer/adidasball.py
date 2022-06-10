from ball import ball 
from bean import injection

@injection
class adidasball(ball):

    def __init__(self):
        self.ball : str = "adidas"

    def get(self):
        return self.ball
