from __future__ import division
import argparse
import math
from datetime import datetime
from decimal import Decimal
from multiprocessing import Process, Queue


def calculate_el(n):
    # Chudonovsky brothers formula for calculating Pi
    left = (Decimal(-1))**Decimal(n) * (Decimal(math.factorial(6*n))) / (Decimal(math.factorial(3*n)) * Decimal(math.factorial(n)) ** 3)
    right = (Decimal(13591409) + Decimal(545120134) * n) / Decimal(640320**3)**Decimal(n+0.5)
    return left * right

def calculate_subset(q, thread_id, list_to_calc, quiet_mode):
    thread_start_time = datetime.now()
    product = 0
    if not quiet_mode:
        print 'Starting thread %s' % thread_id

    for el in list_to_calc:
        product += calculate_el(el)

    if not quiet_mode:
        print 'Thread %s has finished' % thread_id 
        print 'Thread %s execution time was  %s (milliseconds)' % (thread_id, calculate_time_elapsed(thread_start_time, datetime.now()))
    q.put(product)
     
            
def divide_list(l, n):
    # i index
    # n step size
    return [l[i::n] for i in xrange(n)]

def calculate_time_elapsed(started, ended):
    return int((ended - started).total_seconds()* 1000)

def persist_pi(output_file, value):
    if output_file is None:
        output_file = 'result.txt'
    with open(output_file, 'w') as out:
        out.write('%s \n' % value)

def main() :

    starting_time = datetime.now()

    parser = argparse.ArgumentParser(description='Multithreaded calculation of pi')
    parser.add_argument('-p', help='Specify presion')
    parser.add_argument('-t', help='Number of threads')
    parser.add_argument('-o', help='Output file')
    parser.add_argument('-q', help='Quiet mode', action='store_true')
    args = parser.parse_args()

    # Default number of threads is 1
    if not args.t:
        args.t = 1
    if not args.p:
        raise Exception('Number of elements mus be specified')

    threads = []
    accuracy_list = range(int(args.p))
    divided = divide_list(accuracy_list, int(args.t))

    q = Queue(int(args.t)) # Max size is the number of threads

    for i in xrange(1,int(args.t) + 1):
        thread = Process(target=calculate_subset, args=(q, i, divided[i - 1], args.q, ))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    total_sum = 0

    while not q.empty():
        total_sum += q.get()

    pi =  1 / (12*total_sum)

    if  not args.q:
        # If not in quiet mode
        print 'Math.pi: %10.40f' % math.pi
        print 'Pi:      %10.40f' % pi
        print 'Threads used: %s' % args.t

    print 'Calculation finished! %s (milliseconds)' % (calculate_time_elapsed(starting_time, datetime.now()))
    # Persist pi value
    persist_pi(args.o, pi)
if __name__ == '__main__':
    main()