import multiprocessing as mp
import multiprocessing
from time import sleep

class B():
    def test_function(self,index):
        print("hello world : %s"%index)

class A(B):
    def __init__(self):


        for i in range(10):
            x = multiprocessing.Process(target=self.test_function, args=(i,))
            x.start()










if __name__ == '__main__':
    a = A()
   