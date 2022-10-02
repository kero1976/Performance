from audioop import mul
import logging
import multiprocessing
import time

"""
サンプル4
・プロセス間通信1
  スレッドと同じやり方だとdはそれぞれのプロセスで作成されているので、共有されていない。
"""

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(processName)-20s: %(message)s')

def worker1(d,lock):
  with lock:
    i = d['x']
    time.sleep(2)
    d['x'] = i + 1
  logging.debug(d)

def worker2(d,lock):
  with lock:
    i = d['x']
    d['x'] = i + 1
  logging.debug(d)

if __name__ == '__main__':
  d = {'x': 0}
  lock = multiprocessing.Lock()
  t1 = multiprocessing.Process(target=worker1, args=(d,lock))
  t2 = multiprocessing.Process(target=worker2, args=(d,lock))
  t1.start()
  t2.start()
  t1.join()
  t2.join()
  logging.debug(d)
