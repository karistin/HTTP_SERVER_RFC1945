from ball import Ball 
from bean import bean

@bean
class Nikeball(Ball):
    def get():
        return 'nikeball'