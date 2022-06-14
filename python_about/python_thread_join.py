import threading, time

class thre():
    name = ''

    def __init__(self, name):
        self.name = name
    
    def run(self):
        for i in range(1, 10):
            print(self.name)
            time.sleep(0.1)
            

if __name__ == '__main__':
    kpu = thre('한국산업기술대학교')
    computer = thre('컴퓨터공학부')
    name = thre('강성준')

    t1 = threading.Thread(target=kpu.run)
    t2 = threading.Thread(target=computer.run)
    t3 = threading.Thread(target=name.run)


    t1.start()
    t2.start()
    t3.start()

    t1.join
    t2.join
    t3.join