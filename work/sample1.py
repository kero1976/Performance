"""
リストに数値を格納し、その数字を取得した処理はその秒数を待って、その後時刻を返して終了する。
0が入ってきたら処理を終了する。
"""
import time
import datetime
import queue
from logging import getLogger, basicConfig, INFO, DEBUG
import threading

logger = getLogger(__name__)

formatter = "%(asctime)s:%(funcName)s:%(message)s"
basicConfig(level=DEBUG, format=formatter)

class Sample1():
    def get_item(self, inquem, outque):
        """
        インプットのキュー処理が終わったことを表すためにtask_downで伝える
        """
        while True:
            i = inque.get()
            self.execute(i, outque)
            if i == 0:
                inque.task_done()
                break
            inque.task_done()

    def execute(self, i, outque):
        time.sleep(i)
        outque.put(datetime.datetime.now())

if __name__ == '__main__':
    logger.debug('START')
    start = time.time()
    listdata = [2,3,3,0, 0]
    inque = queue.Queue()
    for i in listdata:
        inque.put(i)
    outque = queue.Queue()
    sample = Sample1()

    for i in range(3):
        t = threading.Thread(target=sample.get_item, args=(inque, outque))
        t.start()

    # sample.get_item(inque, outque)
    
    print(outque.get())
    print(outque.get())
    print(outque.get())
    inque.join()
    end = time.time()
    logger.debug('END')
    logger.debug('処理時間:{:.2f}'.format(end - start))