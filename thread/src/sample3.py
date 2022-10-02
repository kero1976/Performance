import logging
import threading
import time

"""
サンプル3
・生存中のスレッドの確認(threading.enumerate())
"""
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(threadName)-20s: %(message)s')
def worker1():
    logging.debug('start')
    time.sleep(5)
    logging.debug('end')

def worker2():
    logging.debug('start')
    time.sleep(2)
    logging.debug('end')

if __name__ == '__main__':
    # スレッドをリストに入れて、後でjoinするのに使用するやり方(面倒)
    # threads = []
    # for _ in range(5):
    #     t = threading.Thread(target=worker1)
    #     t.setDaemon(True)
    #     t.start()
    #     threads.append(t)

    # for thread in threads:
    #     thread.join()

    for _ in range(5):
        t = threading.Thread(target=worker1)
        t.setDaemon(True)
        t.start()
    print(threading.enumerate())
    for thread in threading.enumerate():
        # メインスレッドも取得するので、メインスレッドはjoinしない
        if thread is threading.currentThread():
            print(thread)
            continue
        thread.join()
