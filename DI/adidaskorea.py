from adidasball import Adidasball
from bean import bean


@bean
class AdidasKorea(Adidasball):
    def get(self):
        return 'AdidasKorea ball'

