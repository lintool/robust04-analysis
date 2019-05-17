"""
Generate scatter plots for reported effectiveness of Robust04
"""
from __future__ import print_function
import matplotlib
import matplotlib.pyplot as plt
from numpy.polynomial import Polynomial
from matplotlib.collections import LineCollection
import argparse
import json
import re
import numpy as np


def find_time(short_cite):
    m = re.search('(\d+)\)', short_cite)
    t = int(m.group(1)) - 2005
    return t


def get_performance(paper_info, use_neural):
    effectiveness = []
    baseline = []
    time = []
    for single_paper_info in paper_info:
        if single_paper_info['standard_setting'] == 'no':
            continue
        is_neural = ( single_paper_info['is_neural'] == 'yes' )
        if is_neural == use_neural:
            try:
                best_ap = single_paper_info['best']['AP']
                baseline_ap = single_paper_info['baseline']['AP']
            except KeyError:
                continue
                # ignore papers without AP when plotting
            else:
                effectiveness.append(best_ap)
                baseline.append(baseline_ap)
                time.append( find_time(single_paper_info['short_cite']))

    return effectiveness, baseline, time




def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--metric','-m', default='AP')
    parser.add_argument('--json_file','-jf',default='robust04_papers.json')
    parser.add_argument('--destfile_name','-df',default='scatter')
    args=parser.parse_args()

    fig, ax = plt.subplots(figsize=[15,5])
    # fig.set_rasterized(True)
    # ax.set_rasterized(True)

    paper_info = json.load(open(args.json_file))

    no_nn_performance, no_nn_baseline, no_nn_time =  get_performance(paper_info, False)
    print ('There are {} non-neural papers'.format(len(no_nn_performance)))

    delta = 0.25
    method_alpha = 0.8
    baseline_alpha = 0.3

    plt.plot([no_nn_time[i]  + delta for i in range(len(no_nn_time))], no_nn_performance, 'ro', label='non-neural models', alpha=method_alpha)
    plt.scatter([no_nn_time[i]  - delta for i in range(len(no_nn_time))], no_nn_baseline, facecolors='none', edgecolors='r', alpha=baseline_alpha)
    no_nn_lines = [ [ (no_nn_time[i]  - delta, no_nn_baseline[i]) , (no_nn_time[i]  + delta, no_nn_performance[i]) ] for i in range(len(no_nn_time) )  ]
    no_nn_lc = LineCollection(no_nn_lines, colors=['red']*len(no_nn_lines), alpha=baseline_alpha)
    ax.add_collection(no_nn_lc)
    no_nn_p = Polynomial.fit(no_nn_time, no_nn_performance,1)
    plt.plot(*no_nn_p.linspace(), color='red', linewidth=2)
    print (no_nn_p)

    nn_performance, nn_baseline, nn_time =  get_performance(paper_info, True)
    print ('There are {} neural papers'.format(len(nn_performance)))

    plt.plot([nn_time[i] + delta for i in range(len(nn_time))], nn_performance, 'bo', label='neural models', alpha=method_alpha)
    plt.scatter([nn_time[i]  - delta for i in range(len(nn_time))], nn_baseline, facecolors='none', edgecolors='blue', alpha=baseline_alpha)
    nn_lines = [ [ (nn_time[i]  - delta, nn_baseline[i]) , (nn_time[i]  + delta, nn_performance[i]) ] for i in range(len(nn_time) ) if  nn_baseline[i] >= 0.15 ]
    nn_lc = LineCollection(nn_lines, colors=['blue']*len(nn_time), alpha=baseline_alpha)
    ax.add_collection(nn_lc)
    nn_p = Polynomial.fit(nn_time, nn_performance,1)
    print (nn_p)
    plt.plot(*nn_p.linspace(), color='b', linewidth=2)
    

    plt.axhline(y=0.333, color='k', linestyle='-', label='TREC best')
    plt.axhline(y=0.258, color='k', linestyle=':', label='TREC median')
    plt.axhline(y=0.2903, color='k', linestyle='-.', label='Anserini RM3')



    # change ticks to years
    years = [  str(y).zfill(2) for y in range(5,20) ]
    plt.xticks( np.arange(len(years))  , years )

    # add different shades to different years
    shade = [0.0, 0.15]
    idx = 0
    for i in range(len(years)):
        plt.axvspan(i - 0.5, i + 0.5, facecolor='k',alpha=shade[idx % 2])
        idx += 1

    plt.ylim(0.2, 0.41)
    plt.xlim(left = -.5, right=len(years) - 0.5)
    plt.xlabel('Year')
    plt.ylabel(args.metric)
    plt.legend(loc=1)
    # plt.savefig('{}.eps'.format(args.destfile_name),  bbox_inches='tight', format='eps', rasterized=True)
    # plt.savefig('{}.svg'.format(args.destfile_name),  bbox_inches='tight', format='svg')
    plt.savefig('{}.pdf'.format(args.destfile_name),  bbox_inches='tight', format='pdf')


if __name__ == '__main__':
    main()
