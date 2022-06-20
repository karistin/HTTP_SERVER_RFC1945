from soccerplayer import Soccerplayer
# from nikeball import Nikeball
from adidasball import Adidasball
from bean import bean, init_bean, get_bean


if __name__ == "__main__":
    init_bean()
    print(get_bean(Soccerplayer).ball.get())
    
