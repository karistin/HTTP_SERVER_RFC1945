# 파이썬 의존성 주입
       
``` bash 
python app.py 
```

```python
from soccerplayer import Soccerplayer
from nikeball import Nikeball
# from adidasball import Adidasball
from adidaskorea import AdidasKorea
from bean import get_bean, initbean

if __name__ == "__main__":
    initbean()
    print(get_bean(Soccerplayer).ball.get())
```
- app.py에서 무엇을 import 하냐에 따라 nike, adidaskorea가 된다.
- @bean으로 등록하고 get_bean에서 의존성을 자동으로 찾아서(알맞은 인터페이스로) 주입한다. 

    
