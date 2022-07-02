from soccerplayer import Soccerplayer
from nikeball import Nikeball
# from adidasball import Adidasball
from adidaskorea import AdidasKorea
from bean import get_bean, initbean


if __name__ == "__main__":
    initbean()
    print(get_bean(Soccerplayer).ball.get())
    
