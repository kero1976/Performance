import logging
import threading
import time

"""
サンプル4
・タイマー(指定した秒数を待ってからスレッドを起動する)
"""
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(threadName)-20s: %(message)s')
def worker1(x, y, z):
    logging.debug('start')
    logging.debug('x:{}'.format(x))
    logging.debug('y:{}'.format(y))
    logging.debug('z:{}'.format(z))
    time.sleep(5)
    logging.debug('end')

def worker2(x, y):
    logging.debug('start')
    logging.debug(x)
    logging.debug(y)
    time.sleep(2)
    logging.debug('end')

if __name__ == '__main__':
    logging.debug('main start')
    # kwargsはdictを展開して引数に渡している
    t1 = threading.Timer(3, worker1, args=(100,), kwargs={'z':200, 'y': 300})
    t1.start()

    t2 = threading.Timer(1, worker2, args=(100,300))
    t2.start()
    logging.debug('main end')