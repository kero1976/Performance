import logging
import threading
import time

"""
サンプル9
・コンディション
  イベントとロックの組み合わせ
  あるスレッドで事前準備を行い、準備ができたことを他のスレッドに伝える(イベントと同じ)
  conditionはwithステートメントを使う(ロックと同じ)
  condition.wait()で待機し、condition.notify_all()※が行われた後に動き出す
  ※notifyAll()だと警告が出た。バージョンによって変わった？
  worker1とworker2はロックを取得できた方から動き出す
"""
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(threadName)-20s: %(message)s')

def worker1(condition):
    with condition:
        condition.wait()
        logging.debug('start')
        time.sleep(1)
        logging.debug('end')

def worker2(condition):
    with condition:
        condition.wait()
        logging.debug('start')
        time.sleep(1)
        logging.debug('end')

def worker3(condition):
    with condition:
        logging.debug('start')
        time.sleep(3)
        logging.debug('end')
        condition.notify_all()


if __name__ == '__main__':
    condition = threading.Condition()
    t1 = threading.Thread(target=worker1, args=(condition,))
    t2 = threading.Thread(target=worker2, args=(condition,))
    t3 = threading.Thread(target=worker3, args=(condition,))
    t1.start()
    t2.start()
    t3.start()

