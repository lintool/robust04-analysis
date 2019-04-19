"""
count the number of papers in certain condition ( neural/non-neural/all papers that are lower/higher than a threshold)
"""
from __future__ import print_function
import matplotlib
import matplotlib.pyplot as plt
from numpy.polynomial import Polynomial
from matplotlib.collections import LineCollection
import random
#from matplotlib.patches import Ellipse, Polygon
import argparse
import sys
import re
import numpy as np


def get_numbers(readme_file, metric, use_neural, compare_baseline):
    if compare_baseline:
        return get_baseline(readme_file, metric, use_neural)
    else:
        return get_performance(readme_file, metric, use_neural)

def get_performance(readme_file, metric, use_neural):
    performance = []
    is_header = True
    with open(readme_file) as f:
        for line in f:
            line = line.strip()
            if 'Best Baseline Effectiveness' in line:
                break
            # skip non data line
            if not line or line[0] != '|':
                continue
            line = line.strip('|')
            cols = line.split('|')
            for i in range(len(cols)):
                cols[i] = cols[i].strip()
            if is_header:
                is_header = False
                try:
                    idx = cols.index(metric)
                except ValueError:
                    print ('metric {} cannot be found!'.format(metric))
                    print ('line is:\n{}'.format(line))
                    sys.exit(-1)
                    
            else:
                if '?' in line:
                    continue
                if use_neural and cols[2] == 'no':
                    continue
                if not use_neural and cols[2] == 'yes':
                    continue 
                try:
                    paper_performance = float(cols[idx])
                except (IndexError, ValueError) as e :
                    continue
                else:
                    performance.append(paper_performance)


    return  performance

def get_baseline(readme_file, metric, use_neural):
    performance = []
    is_header = True
    in_second_table = False
    with open(readme_file) as f:
        for line in f:
            line = line.strip()
            if 'Best Baseline Effectiveness' in line:
                in_second_table = True
                continue

            if not in_second_table:
                continue
            # skip non data line
            if not line or line[0] != '|':
                continue
            line = line.strip('|')
            cols = line.split('|')
            for i in range(len(cols)):
                cols[i] = cols[i].strip()
            if is_header:
                is_header = False
                try:
                    idx = cols.index(metric)
                except ValueError:
                    print ('metric {} cannot be found!'.format(metric))
                    print ('line is:\n{}'.format(line))
                    sys.exit(-1)
                    
            else:
                if '?' in line:
                    continue
                if use_neural and cols[2] == 'no':
                    continue
                if not use_neural and cols[2] == 'yes':
                    continue 

                try:
                    
                    paper_performance = float(cols[idx])
                except (IndexError, ValueError) as e :
                    continue
                else:
                    performance.append(paper_performance)


    return  performance

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--metric','-m', default='AP')
    parser.add_argument('--readme_file','-rf',default='README.md')
    parser.add_argument('--models', '-md' ,choices=['all','non-neural', 'neural'])
    parser.add_argument('--compare_baseline', '-cb' ,action='store_true')
    parser.add_argument('--condition', '-c', choices=['lower', 'higher'])
    parser.add_argument('value',type=float)
    args=parser.parse_args()

    # TREC best 0.333
    # TREC median 0.258
    # Anserini RM3 0.2903


    if args.models == 'non-neural':
        performance = get_numbers(args.readme_file, args.metric, False, args.compare_baseline)
    elif args.models == 'neural':
        performance = get_numbers(args.readme_file, args.metric, True, args.compare_baseline)
    else:
        performance = get_numbers(args.readme_file, args.metric, False, args.compare_baseline)
        performance += get_numbers(args.readme_file, args.metric, True, args.compare_baseline)

    result_list = []
    if args.condition == 'lower':
        result_list = list(filter(lambda x: x < args.value, performance))
    else:
        result_list = list(filter(lambda x: x > args.value, performance))
    print (sorted(result_list))
    print ('{} out of {} queries satisfied ({:.1%})'.format(len(result_list), len(performance), len(result_list) *1.0/len(performance)))


if __name__ == '__main__':
    main()
