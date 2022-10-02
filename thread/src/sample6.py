import logging
import threading
import time

"""
サンプル6
・セマフォ
  ロックを取得できる数を指定できる
"""
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(threadName)-20s: %(message)s')
def worker1(semaphore):
    with semaphore:
        logging.debug('start')
        time.sleep(3)
        logging.debug('end')

def worker2(semaphore):
    with semaphore:
        logging.debug('start')
        time.sleep(3)
        logging.debug('end')

def worker3(semaphore):
    with semaphore:
        logging.debug('start')
        time.sleep(3)
        logging.debug('end')

if __name__ == '__main__':
    semaphore = threading.Semaphore(2)
    t1 = threading.Thread(target=worker1, args=(semaphore,))
    t2 = threading.Thread(target=worker2, args=(semaphore,))
    t3 = threading.Thread(target=worker3, args=(semaphore,))
    t1.start()
    t2.start()
    t3.start()


