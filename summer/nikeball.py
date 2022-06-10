from ball import ball 
from bean import injection


@injection
class nikeball(ball):

    def __init__(self):
        self.ball : str = "nike"

    def get(self):
        return self.ball
