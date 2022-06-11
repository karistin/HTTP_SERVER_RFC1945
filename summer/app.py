# from nikeball import Nikeball
from adidasball import Adidasball
from soccerplayer import Soccerplayer
from bean import get_bean


if __name__ == "__main__":
    print(get_bean(Soccerplayer()).ball.get(None))
    # get_bean(Soccerplayer).ball.get()
    
