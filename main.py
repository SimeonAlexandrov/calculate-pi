import argparse
import time
from datetime import datetime
from threading import Thread

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

    def calculate_sum_el(self,n):
        # Chudonovsky brothers formula for calculating Pi
        time.sleep(2)
        print n
        return 5*n
    
    def calculate_all(self):
        for el in self.list_to_calc:
            self.product += self.calculate_sum_el(el)



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
    
    pi=0
    for th in threads:
        pi += th.join()

    print 'Pi: %d' % pi
    print 'Calculation finished! %s' % (datetime.now() - starting_time)
    print 'Threads used: %s' % args.t


if __name__ == '__main__':
    main()