from multiprocessing import (
    process,
    Lock, RLock, Semaphore, Queue, Event, Condition, Barrier,
    Value, Array, Pipe, Manager
)

import logging
import multiprocessing
import time

"""
サンプル1
Lock, RLock, Semaphore, Queue, Event, Condition, Barrier,はスレッドと同じように使えるので省略
・プロセスに名前を設定する方法
・プロセスに引数を渡す方法
・プロセスのデーモン化
"""

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(processName)-20s: %(message)s')
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
    # プロセスに名前を指定
    t1 = multiprocessing.Process(name='rename worker1', target=worker1)
    # デーモン化もスレッドと同じように使える
    t1.daemon = True
    # プロセスに引数を指定
    t2 = multiprocessing.Process(target=worker2, args=(100, ), kwargs={'y': 200})
    t1.start()
    t2.start()
    print('started')
    t1.join()