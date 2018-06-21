import os   
from decimal import *
from datetime import datetime
import requests

def calculate_el(n):
    # Chudonovsky brothers formula for calculating Pi
    left = (Decimal(-1))**Decimal(n) * (Decimal(math.factorial(6*n))) / (Decimal(math.factorial(3*n)) * Decimal(math.factorial(n)) ** 3)
    right = (Decimal(13591409) + Decimal(545120134) * n) / Decimal(640320**3)**Decimal(n+0.5)
    return left * right

def calculate_all(subset):
    for el in subset:
        product += calculate_el(el)

def main():
    starting_time = datetime.now()

    acc = os.environ['ACCURACY']
    n = os.environ['NUMBER_OF_TASKS']
    id = os.environment['TASK_ID']  

    whole_list = range(acc)
    subsets = [whole_list[i::n] for i in xrange(n)]
    print subsets[id]

    node_product = calculate_all(subsets[id])
    print 'Calculation finished! %s' % (datetime.now() - starting_time)
    print node_product

    # TODO send request to server with result
if __name__ == '__main__':
    main()