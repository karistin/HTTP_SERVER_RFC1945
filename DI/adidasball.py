from ball import Ball 
from bean import bean


@bean
class Adidasball(Ball):
    def get(self):
        return 'adidasball'