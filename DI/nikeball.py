from ball import Ball 
from bean import bean


@bean
class Nikeball(Ball):
    def get(self):
        return 'nikeball'