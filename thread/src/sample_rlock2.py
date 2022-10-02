
import threading

lock = threading.RLock()

def factorial(num):
    """
    階乗計算
    3! = 3*2*1=6
    """
    with lock:
        if num == 1:
            return 1
        else:
            return num * factorial(num -1)

print(factorial(5))