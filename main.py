from __future__ import division
import argparse
import time
import math
from datetime import datetime
from threading import Thread
from decimal import *

class CalculationThread(Thread):

    def __init__(self, thread_id, list_to_calc):
        Thread.__init__(self)
        self.thread_id = thread_id
        self.list_to_calc = list_to_calc
        self.product = 0

    def run(self):
        print 'Starting thread %s' % self.thread_id
        self.calculate_all()
        print 'Thread %s has finished' % self.thread_id 

    def join(self):
        Thread.join(self)
        return self.product

    def calculate_el(self,n):
        # Chudonovsky brothers formula for calculating Pi
        left = (Decimal(-1))**Decimal(n) * (Decimal(math.factorial(6*n))) / (Decimal(math.factorial(3*n)) * Decimal(math.factorial(n)) ** 3)
        right = (Decimal(13591409) + Decimal(545120134) * n) / Decimal(640320**3)**Decimal(n+0.5)
        return left * right
    
    def calculate_all(self):
        for el in self.list_to_calc:
            self.product += self.calculate_el(el)



def divideList(l, n):
    # i index
    # n step size
    return [l[i::n] for i in xrange(n)]

def main():
    starting_time = datetime.now()

    parser = argparse.ArgumentParser(description='Multithreaded calculation of pi')
    parser.add_argument('-p', help='Specify accuracy')
    parser.add_argument('-t', help='Number of threads')
    parser.add_argument('-o', help='Output file')
    parser.add_argument('-q', help='Quiet mode')
    args = parser.parse_args()

    threads = []
    accuracy_list = range(int(args.p))
    divided = divideList(accuracy_list, int(args.t))

    for i in xrange(1,int(args.t) + 1):
        thread = CalculationThread(i, divided[i - 1])
        threads.append(thread)

    for th in threads:
        th.start()
    
    sums=0
    for th in threads:
        sums += th.join()
    pi =  1 / (12*sums)
    print 'Stock pi: %10.40f' % math.pi
    print 'Pi:       %10.40f' % pi
    print 'Calculation finished! %s' % (datetime.now() - starting_time)
    print 'Threads used: %s' % args.t


if __name__ == '__main__':
    main()