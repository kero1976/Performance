import logging
import threading
import time

"""
サンプル8
・イベント
  あるスレッドで事前準備を行い、準備ができたことを他のスレッドに伝える
  event.wait()で待機し、event.set()が行われた後に動き出す
  worker1とworker2は同時に動き出す
"""
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(threadName)-20s: %(message)s')

def worker1(event):
    event.wait()
    logging.debug('start')
    time.sleep(1)
    logging.debug('end')

def worker2(event):
    event.wait()
    logging.debug('start')
    time.sleep(1)
    logging.debug('end')

def worker3(event):
    logging.debug('start')
    time.sleep(3)
    logging.debug('end')
    event.set()


if __name__ == '__main__':
    event = threading.Event()
    t1 = threading.Thread(target=worker1, args=(event,))
    t2 = threading.Thread(target=worker2, args=(event,))
    t3 = threading.Thread(target=worker3, args=(event,))
    t1.start()
    t2.start()
    t3.start()

