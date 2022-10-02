import logging
import multiprocessing
import time

"""
サンプル2
・ワーカープロセスのプールで非同期（apply_async）
  get()は待ち続けるので、timeout指定でエラーにすることも可能
・同期でブロック（apply）
"""

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(processName)-20s: %(message)s')

def worker1(i):
    logging.debug('start')
    time.sleep(5)
    logging.debug('end')
    return i

if __name__ == '__main__':
    with multiprocessing.Pool(5) as p:
        # 同期(apply)はブロックして値を返す。executed applyはすぐには表示されない
        logging.debug(p.apply(worker1, (200,)))
        logging.debug('executed apply')

        # 非同期(apply_async)はブロックしない。executedはすぐに表示される。値はgetで取得する
        p1 = p.apply_async(worker1, (100,))
        p2 = p.apply_async(worker1, (100,))
        logging.debug('executed')
        logging.debug(p1.get(timeout=10))
        logging.debug(p2.get())
