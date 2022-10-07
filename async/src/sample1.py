import logging
import threading
import time
import multiprocessing
import asyncio

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(processName)-20s: %(threadName)-20s %(message)s')

loop = asyncio.get_event_loop()

def worker():
    logging.debug('start')
    time.sleep(2)
    logging.debug('end')

def single():
    worker()
    worker()

def thread():
    t1 = threading.Thread(target=worker)
    t2 = threading.Thread(target=worker)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

def process():
    p1 = multiprocessing.Process(target=worker)
    p2 = multiprocessing.Process(target=worker)
    p1.start()
    p2.start()
    p1.join()
    p2.join()

async def asyncworker():
    logging.debug('start')
    await asyncio.sleep(2)
    logging.debug('end')

if __name__ == '__main__':
    start = time.time()
    loop.run_until_complete(asyncio.wait([asyncworker(), asyncworker()]))
    loop.close()
    end = time.time()
    logging.debug('time:{:.4f}'.format(end - start))