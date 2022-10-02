import logging
import threading
import time

"""
サンプル1
・スレッドに名前を設定する方法
・スレッドに引数を渡す方法
"""
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(threadName)-20s: %(message)s')
def worker1():
    logging.debug('start')
    time.sleep(5)
    logging.debug('end')

def worker2(x, y=1):
    logging.debug('start')
    logging.debug(x)
    logging.debug(y)
    time.sleep(5)
    logging.debug('end')

if __name__ == '__main__':
    # スレッドに名前を指定
    t1 = threading.Thread(name='rename worker1', target=worker1)
    # スレッドに引数を指定
    t2 = threading.Thread(target=worker2, args=(100, ), kwargs={'y': 200})
    t1.start()
    t2.start()
    print('started')
