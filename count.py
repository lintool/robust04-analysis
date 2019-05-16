"""
Convert the json file to MD for readibility
"""

from __future__ import print_function
import argparse
import json
from collections import OrderedDict

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--json_file','-jf',default='robust04_papers.json')
    args=parser.parse_args()

    papers = json.load(open(args.json_file))

    total = 0
    standard = 0
    standard_ap = 0
    neural = 0
    notneural = 0
    baseline_below_trec_median = 0
    below_trec_median = 0
    below_anserini_rm3base = 0
    above_trec_best = 0

    highest = 0

    neural_below_trec_median = 0
    neural_baseline_below_trec_median = 0
    neural_below_anserini_rm3base = 0

    below_xfold_neural = 0
    below_xfold_all = 0

    below_drmm_neural = 0
    below_drmm_all = 0

    for paper in papers:
        total += 1
        if paper['standard_setting'] == 'yes':
            standard += 1
            if 'best' in paper and 'AP' in paper['best']:
                standard_ap += 1
                if paper['is_neural'] == 'yes':
                    neural += 1
                else:
                    notneural += 1

                if paper['baseline']['AP'] < 0.258:
                    baseline_below_trec_median += 1
                    if paper['is_neural'] == 'yes':
                        neural_baseline_below_trec_median += 1

                if paper['best']['AP'] < 0.258:
                    below_trec_median += 1
                    if paper['is_neural'] == 'yes':
                        neural_below_trec_median += 1

                if paper['best']['AP'] < 0.2903:
                    below_anserini_rm3base += 1
                    if paper['is_neural'] == 'yes':
                        neural_below_anserini_rm3base += 1

                if paper['best']['AP'] > 0.333:
                    above_trec_best += 1

                if paper['best']['AP'] > highest:
                    highest = paper['best']['AP']

                if paper['best']['AP'] < 0.3033:
                    below_xfold_all += 1
                    if paper['is_neural'] == 'yes':
                        below_xfold_neural += 1

                if paper['best']['AP'] < 0.3152:
                    below_drmm_all += 1
                    if paper['is_neural'] == 'yes':
                        below_drmm_neural += 1

    print('Total number of papers: {}'.format(total))
    print('Standard Settings: {}'.format(standard))
    print('Standard Settings + AP: {}'.format(standard_ap))
    print('----------------------------')
    print('Neural: {}'.format(neural))
    print('Non-neural: {}'.format(notneural))
    print('----------------------------')
    print('Highest AP: {}'.format(highest))
    print('----------------------------')
    print('All, baseline lower than TREC median:        {} ({:4.1f}%)'.format(baseline_below_trec_median, baseline_below_trec_median/standard_ap*100))
    print('All, best lower than TREC median:            {} ({:4.1f}%)'.format(below_trec_median, below_trec_median/standard_ap*100))
    print('All, best lower than Anseirni RM default:    {} ({:4.1f}%)'.format(below_anserini_rm3base, below_anserini_rm3base/standard_ap*100))
    print('All, higher than TREC best:                   {} ({:4.1f}%)'.format(above_trec_best, above_trec_best/standard_ap*100))
    print('----------------------------')
    print('Neural, baseline lower than TREC median:      {} ({:4.1f}%)'.format(neural_baseline_below_trec_median, neural_baseline_below_trec_median/neural*100))
    print('Neural, best lower than TREC median :         {} ({:4.1f}%)'.format(neural_below_trec_median, neural_below_trec_median/neural*100))
    print('Neural, best lower than Anseirni RM default: {} ({:.1f}%)'.format(neural_below_anserini_rm3base, neural_below_anserini_rm3base/neural*100))
    print('----------------------------')
    print('All, below xfold:         {} ({:4.1f}%)'.format(below_xfold_all, below_xfold_all/standard_ap*100))
    print('Neural, below xfold:      {} ({:4.1f}%)'.format(below_xfold_neural, below_xfold_neural/neural*100))
    print('All, below DRMM:          {} ({:4.1f}%)'.format(below_drmm_all, below_drmm_all/standard_ap*100))
    print('Neural, below DRMM:       {} ({:4.1f}%)'.format(below_drmm_neural, below_drmm_neural/neural*100))

if __name__ == '__main__':
    main()
