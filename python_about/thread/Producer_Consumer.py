import threading
import random
import time


class Producer(threading.Thread):

    def __init__(self, intergers, condition):
        threading.Thread.__init__(self)
        self.intergers = intergers
        self.condition = condition

    def run(self):
        while True:
            interger = random.randint(0, 256)

            self.condition.acquire()

            print(f'condition acquired by {self.name}')

            self.intergers.append(interger)

            print(f'{interger} appended to list by {self.name}')

            self.condition.notifyAll()

            print(f'condition released by {self.name}')

            self.condition.release()
            time.sleep(1)


class Consumer(threading.Thread):

    def __init__(self, intergers, condition):
        threading.Thread.__init__(self)
        self.intergers = intergers
        self.condition = condition
    
    def run(self):
        while True:
            self.condition.acquire()
            if self.intergers:
                integer = self.intergers.pop()
                print(f'{integer} popped from list by P{self.name}')
                break
            print(f'condition wait by {self.name}')

            self.condition.wait()
        
        print(f'condition released by {self.name}')

        self.condition.release()


def main():
    integers = []
    condition = threading.Condition()
    print(condition.__annotations__)
    t1 = Producer(integers, condition)
    t2 = Consumer(integers, condition)

    t1.start()
    t2.start()

    t1.join()
    t2.join()


if __name__ == '__main__':
    main()