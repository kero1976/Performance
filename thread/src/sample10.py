import logging
import threading
import time

"""
サンプル10
・バリア
  指定した数のスレッドが起動するまで待機する
  wait()が呼ばれるとBarrierで指定した数が1減り、0になると動き出す。
  サーバとクライアントのスレッドをセットで同時に起動したい時などに使う。
"""
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(threadName)-20s: %(message)s')

def worker1(barrier):
    r = barrier.wait()
    logging.debug('num={}'.format(r))
    while True:
        logging.debug('start')
        time.sleep(1)
        logging.debug('end')

def worker2(barrier):
    r = barrier.wait()
    logging.debug('num={}'.format(r))
    while True:
        logging.debug('start')
        time.sleep(1)
        logging.debug('end')

if __name__ == '__main__':
    barrier = threading.Barrier(2)
    t1 = threading.Thread(target=worker1, args=(barrier,))
    t2 = threading.Thread(target=worker2, args=(barrier,))
    t1.start()
    t2.start()


