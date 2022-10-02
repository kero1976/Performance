import threading
import logging
import time

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(threadName)-20s: %(message)s')

class X:
    """
    クラス外からスレッドセーフなアクセスを持ち、クラス内から同じメソッドを使用したい場合：
    自分の理解
      changeAとchangeBは外部から呼ばれてスレッドセーフにしたいので、ロックが必要
      changeAandBというスレッドセーフなメソッドも必要で、この中でchangeAとchangeBを呼んでいる
      ロックを2種類用意すると、changeAandBを呼んだ瞬間に、changeAとchangeBを呼べることになってしまう。
    """
    def __init__(self):
        self.a = 1
        self.b = 2
        self.lock = threading.RLock()

    def changeA(self):
        with self.lock:
            self.a = self.a + 1
            logging.debug('a:{}, b:{}'.format(self.a, self.b))

    def changeB(self):
        with self.lock:
            self.b = self.b + self.a
            logging.debug('b:{},  a:{}'.format(self.b, self.a))

    def changeAandB(self):
        # you can use chanceA and changeB thread-safe!
        with self.lock:
            self.changeA() # a usual lock would block at here
            self.changeB()

def worker1(x):
    logging.debug('start')
    for _ in range(5):
        x.changeA()
        x.changeAandB()
        # time.sleep(1)
    logging.debug('end')

def worker2(x):
    logging.debug('start')
    for _ in range(5):
        x.changeB()
        x.changeAandB()
        # time.sleep(1)
    logging.debug('end')

if __name__ == '__main__':
    """
    aは必ず16
    bはタイミングにより異なる。例:133, 136, 139など
    """
    x = X()
    t1 = threading.Thread(target=worker1, args=(x,))
    t2 = threading.Thread(target=worker2, args=(x,))
    t1.start()
    t2.start()