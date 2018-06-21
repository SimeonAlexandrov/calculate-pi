from __future__ import division
import argparse
import time
import math
from datetime import datetime
from threading import Thread
from decimal import *

class CalculationThread(Thread):

    def __init__(self, thread_id, list_to_calc, quiet_mode):
        Thread.__init__(self)
        self.thread_id = thread_id
        self.list_to_calc = list_to_calc
        self.product = 0
        self.time_started = datetime.now()
        self.quiet_mode = quiet_mode

    def run(self):
        if not self.quiet_mode:
            print 'Starting thread %s' % self.thread_id
        self.calculate_all()
        if not self.quiet_mode:
            print 'Thread %s has finished' % self.thread_id 

    def join(self):
        Thread.join(self)
        if not self.quiet_mode:
            print 'Thread %s execution time was  %s (milliseconds)' % (self.thread_id, calculate_time_elapsed(self.time_started, datetime.now()))
        return self.product

    def calculate_el(self,n):
        # Chudonovsky brothers formula for calculating Pi
        left = (Decimal(-1))**Decimal(n) * (Decimal(math.factorial(6*n))) / (Decimal(math.factorial(3*n)) * Decimal(math.factorial(n)) ** 3)
        right = (Decimal(13591409) + Decimal(545120134) * n) / Decimal(640320**3)**Decimal(n+0.5)
        return left * right
    
    def calculate_all(self):
        for el in self.list_to_calc:
            self.product += self.calculate_el(el)

            
def divide_list(l, n):
    # i index
    # n step size
    return [l[i::n] for i in xrange(n)]

def calculate_time_elapsed(started, ended):
    return (ended - started).total_seconds()* 1000

def persist_pi(output_file, value):
    if output_file is None:
        output_file = 'result.txt'
    with open(output_file, 'w') as out:
        out.write('%s \n' % value)

def main():
    starting_time = datetime.now()

    parser = argparse.ArgumentParser(description='Multithreaded calculation of pi')
    parser.add_argument('-p', help='Specify presion')
    parser.add_argument('-t', help='Number of threads')
    parser.add_argument('-o', help='Output file')
    parser.add_argument('-q', help='Quiet mode', action='store_true')
    args = parser.parse_args()

    threads = []
    accuracy_list = range(int(args.p))
    divided = divide_list(accuracy_list, int(args.t))

    for i in xrange(1,int(args.t) + 1):
        thread = CalculationThread(i, divided[i - 1], args.q)
        threads.append(thread)

    for th in threads:
        th.start()
    
    sums=0
    for th in threads:
        sums += th.join()
    pi =  1 / (12*sums)
    if  not args.q:
        # If not in quiet mode
        print 'Math.pi: %10.40f' % math.pi
        print 'Pi:       %10.40f' % pi
        print 'Threads used: %s' % args.t
    
    print 'Calculation finished! %s (milliseconds)' % (calculate_time_elapsed(starting_time, datetime.now()))
    # Persist pi value
    persist_pi(args.o, pi)

if __name__ == '__main__':
    main()