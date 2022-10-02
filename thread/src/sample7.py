import logging
import queue
import threading
import time

"""
サンプル7
・キュー
  複数スレッドでデータのやり取りを行う
  putでデータを入れてgetで取得する。getでデータを取得できない場合は待つ(データが入らないと終わらない)
  キューにもjoin()がある。join()するためには終わったことを通知するため、キューの数だけtask_done()する必要がある。
  queue.get()でgetした後の処理が終わった後に明示的にtask_done()をする必要がある。getしただけでは処理が終わったかわからないので。
"""
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(threadName)-20s: %(message)s')
def worker1(queue):
    logging.debug('start')
    while True:
        item = queue.get()
        if item is None:
            break
        
        logging.debug(item)
        queue.task_done()

    logging.debug('キュー処理終了後の処理')
    logging.debug('end')



if __name__ == '__main__':
    queue = queue.Queue()
    for i in range(10000):
        queue.put(i)
    ts = []
    for _ in range(3):
        t = threading.Thread(target=worker1, args=(queue,))
        t.start()
        ts.append(t)

    logging.debug('タスク処理中')
    queue.join()
    logging.debug('タスク完了')
    for _ in range(len(ts)):
        queue.put(None)
    
    [t.join() for t in ts]


