import logging
import multiprocessing
import time
import queue

"""
サンプル5
・プロセス間通信2
  キューを使用する(まだ動かない)
"""

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(processName)-20s: %(message)s')

def worker1(queue):
  # d = queue.get()
  # i = d['x']
  # time.sleep(2)
  # d['x'] = i + 1
  # queue.put(d)
  logging.debug('a')

def worker2(queue):
  # d = queue.get()
  # i = d['x']
  # time.sleep(2)
  # d['x'] = i + 1
  # queue.put(d)
  logging.debug('a')

if __name__ == '__main__':
  qu = queue.Queue()
  # d = {'x': 0}
  # queue.put(d)
  t1 = multiprocessing.Process(target=worker1, args=(qu,))
  t2 = multiprocessing.Process(target=worker2, args=(qu,))
  t1.start()
  t2.start()
  t1.join()
  t2.join()
  # logging.debug(queue.get())
