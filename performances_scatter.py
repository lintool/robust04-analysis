"""
Generate scatter plots for reported effectiveness of Robust04
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

def convert_time_to_num(time):
    for i in range(len(time)):
        m = re.search('(\d+)-(\d+)', time[i])
        paper_year = int(m.group(1))
        # paper_month = int(m.group(2))
        # time[i] = paper_year - 5  +  (paper_month * 1.0 / 13 )
        time[i] = paper_year - 5

def check_papers(readme_file):
    names_1 = []
    names_2 = []
    table1 = True
    with open(readme_file) as f:
        for line in f:
            line = line.strip()
            
            if 'Best Baseline Effectiveness' in line:
                table1 = False
                continue
            if not line or line[0] != '|' or 'Paper' in line:
                continue
            line = line.strip('|')
            cols = line.split('|')
            name = cols[0].strip()
            if table1:
                names_1.append(name)
            else:
                names_2.append(name)

    for i in range(len(names_1)):
        if names_1[i] != names_2[i]:
            print ('Wrong paper name at {}'.format(i))
            print (names_1[i])
            print (names_2[i])
            sys.exit(0)


def get_performance(readme_file, metric, use_neural):
    time = []
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
                paper_time = cols[1][2:]
                # month.add(paper_time)
                try:
                    
                    paper_performance = float(cols[idx])
                except (IndexError, ValueError) as e :
                    continue
                else:
                    time.append(paper_time)
                    performance.append(paper_performance)


    convert_time_to_num(time)
    return  performance, time

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
    parser.add_argument('--destfile_name','-df',default='scatter')
    args=parser.parse_args()

    fig, ax = plt.subplots(figsize=[15,5])
    check_papers(args.readme_file)
    no_nn_performance, no_nn_time = get_performance(args.readme_file, args.metric, False)
    no_nn_baseline = get_baseline(args.readme_file, args.metric, False)
    print ('There are {} non-neural papers'.format(len(no_nn_performance)))
    # print (no_nn_performance)
    # print (len(no_nn_performance))
    # print (no_nn_baseline)
    # print (len(no_nn_baseline))

    delta = 0.25
    method_alpha = 0.8
    baseline_alpha = 0.3

    # no_nn_time_for_plot = [ t + random.uniform(-0.25, 0.25) for t in no_nn_time]
    # no_nn_rands = [random.uniform(0, 0.25) for i in range(len(no_nn_time))]
    no_nn_rands = [0 for i in range(len(no_nn_time))]
    # no_nn_time_for_plot = no_nn_time
    plt.plot([no_nn_time[i] + no_nn_rands[i] + delta for i in range(len(no_nn_time))], no_nn_performance, 'ro', label='non-neural models', alpha=method_alpha)
    plt.scatter([no_nn_time[i] - no_nn_rands[i] - delta for i in range(len(no_nn_time))], no_nn_baseline, facecolors='none', edgecolors='r', alpha=baseline_alpha)
    no_nn_lines = [ [ (no_nn_time[i] - no_nn_rands[i] - delta, no_nn_baseline[i]) , (no_nn_time[i] + no_nn_rands[i] + delta, no_nn_performance[i]) ] for i in range(len(no_nn_time) )  ]
    no_nn_lc = LineCollection(no_nn_lines, colors=['red']*len(no_nn_lines), alpha=baseline_alpha)
    ax.add_collection(no_nn_lc)
    no_nn_p = Polynomial.fit(no_nn_time, no_nn_performance,1)
    plt.plot(*no_nn_p.linspace(), color='red', linewidth=2)
    print (no_nn_p)

    nn_performance, nn_time = get_performance(args.readme_file, args.metric, True)
    print ('There are {} neural papers'.format(len(nn_performance)))
    nn_baseline = get_baseline(args.readme_file, args.metric, True)
    nn_rands = [0 for i in range(len(nn_time))]

    plt.plot([nn_time[i] + nn_rands[i] + delta for i in range(len(nn_time))], nn_performance, 'bo', label='neural models', alpha=method_alpha)
    plt.scatter([nn_time[i] - nn_rands[i] - delta for i in range(len(nn_time))], nn_baseline, facecolors='none', edgecolors='blue', alpha=baseline_alpha)
    nn_lines = [ [ (nn_time[i] - nn_rands[i] - delta, nn_baseline[i]) , (nn_time[i] + nn_rands[i] + delta, nn_performance[i]) ] for i in range(len(nn_time) ) if  nn_baseline[i] >= 0.15 ]
    nn_lc = LineCollection(nn_lines, colors=['blue']*len(nn_time), alpha=baseline_alpha)
    ax.add_collection(nn_lc)
    nn_p = Polynomial.fit(nn_time, nn_performance,1)
    print (nn_p)
    plt.plot(*nn_p.linspace(), color='b', linewidth=2)
    
    # add TREC Best
    plt.axhline(y=0.333, color='k', linestyle='-', label='TREC best')
    plt.axhline(y=0.258, color='k', linestyle=':', label='TREC median')
    plt.axhline(y=0.2903, color='k', linestyle='-.', label='Anserini RM3')



    # change ticks to years
    years = [  str(y).zfill(2) for y in range(5,19) ]
    plt.xticks( np.arange(len(years))  , years )

    # add different shades to different years
    shade = [0.0, 0.2]
    idx = 0
    for i in range(len(years)):
        plt.axvspan(i - 0.5, i + 0.5, facecolor='k',alpha=shade[idx % 2])
        idx += 1

    plt.xlim(left = -.5, right=len(years) - 0.5)
    plt.xlabel('Year')
    plt.ylabel(args.metric)
    plt.legend()
    plt.savefig('{}.png'.format(args.destfile_name), bbox_inches='tight')


if __name__ == '__main__':
    main()
