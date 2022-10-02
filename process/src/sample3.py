import logging
import multiprocessing
import time

"""
サンプル3
・ワーカープロセスのプールのマップ
  rのget()を実行してリストに入れているイメージ
・mapも同期と非同期がある
・非同期はtimeout設定が可能
・imapはイテレータを返す
"""

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(processName)-20s: %(message)s')

def worker1(i):
    logging.debug('start')
    time.sleep(5)
    logging.debug('end')
    return i * 2

if __name__ == '__main__':
    with multiprocessing.Pool(5) as p:
        r = p.map(worker1, [100,200])
        logging.debug('executed')
        logging.debug(r)

        r = p.map_async(worker1, [100,200])
        logging.debug('executed async')
        logging.debug(r.get(timeout=10))

        r = p.imap(worker1, [100,200])
        logging.debug('executed imap')
        logging.debug([i for i in r])

        # 非同期(apply_async)はブロックしない。executedはすぐに表示される。値はgetで取得する
        # p1 = p.apply_async(worker1, (100,))
        # p2 = p.apply_async(worker1, (100,))
        # logging.debug('executed')
        # logging.debug(p1.get(timeout=10))
        # logging.debug(p2.get())
