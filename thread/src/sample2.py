import logging
import threading
import time

"""
サンプル2
・スレッドのデーモン化
・joinしないとプログラムがスレッドの終了を待たずに終了する
・joinはデーモン化していないスレッドにも書くことができるが、書かなくてもjoinする
"""
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(threadName)-20s: %(message)s')
def worker1():
    logging.debug('start')
    time.sleep(5)
    logging.debug('end')

def worker2():
    logging.debug('start')
    time.sleep(2)
    logging.debug('end')

if __name__ == '__main__':
    t1 = threading.Thread(target=worker1)
    t1.setDaemon(True)
    t2 = threading.Thread(target=worker2)
    t1.start()
    t2.start()
    print('started')
    # t1.join()を書かないと、t1の終了を待たずに終わる
    t1.join()
    # t2.join()は書いても書かなくても、挙動は変わらない。(デーモン化していなければ終了するまで待つ)
    # t2.join()

