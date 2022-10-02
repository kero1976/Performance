import logging
import threading
import time

"""
サンプル5
・ロック
  グローバルに設定して使うことも可能だが、引数で渡す方法が推奨されている
  lock.acquire()とlock.release()はwithステートメントを使うことも可能
・LockとRLock
  Lockだと1回しかロックできないが、RLockは2回できる。
  Lockはacquireして、解放せずにもう一度acquireするとreleaseするまで待ち続ける。
  RLockが必要なケースは以下。別途サンプルで検証する
    ・クラス外からスレッドセーフなアクセスを持ち、クラス内から同じメソッドを使用したい場合
    ・より明白な再帰のために
"""
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(threadName)-20s: %(message)s')
def worker1(d, lock):
    """
    lock.acquire()とlock.release()を使う方法
    """
    logging.debug('start')
    lock.acquire()
    i = d['x']
    time.sleep(1)
    d['x'] = i + 1
    # Lockを渡していると延々と待ち続ける
    with lock:
        d['x'] = i + 1
    lock.release()
    logging.debug(d)
    logging.debug('end')

def worker2(d, lock):
    """
    with lockを使う方法
    """
    logging.debug('start')
    with lock:
        i = d['x']
        d['x'] = i + 1
    logging.debug(d)
    logging.debug('end')

if __name__ == '__main__':
    d = {'x': 0}
    lock = threading.RLock()
    t1 = threading.Thread(target=worker1, args=(d, lock))
    t2 = threading.Thread(target=worker2, args=(d, lock))
    t1.start()
    t2.start()
    print('started')


