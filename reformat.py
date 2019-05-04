"""
reformat the raw MD file to a JSON file with 
a list of documents following the format below:

{ 
  'short_cite': 'Foo et al. (XYZ 2010)',
  'is_nn_paper': False,
  'baseline': {'ap': 0.2345, ...},
  'best': {'ap': 0.2345, ...}
}

And then generate a 
"""
from __future__ import print_function
#from matplotlib.patches import Ellipse, Polygon
import argparse
import sys
import re
import json
from collections import OrderedDict


def get_paper_info(readme_file):
    paper_data = OrderedDict()
    is_header = True
    in_baseline_table = False


    with open(readme_file) as f:
        for line in f:
            line = line.strip()
            if 'Best Baseline Effectiveness' in line:
                in_baseline_table = True
                is_header = True
                continue

            # skip non data line
            if not line or line[0] != '|' or '?' in line:
                continue
            line = line.strip('|')
            cols = line.split('|')
            for i in range(len(cols)):
                cols[i] = cols[i].strip()
            if is_header:
                is_header = False
                idx_to_metric = {}
                for idx in range(3, len(cols)):
                    metric = cols[idx]
                    idx_to_metric[idx] = metric

            else:
                line_data = parse_data_line(cols, idx_to_metric)
                short_cite = line_data['short_cite'] 
                if in_baseline_table:
                    paper_data[short_cite]['baseline'] = line_data['effectiveness']
                else:
                    paper_data[short_cite] = OrderedDict()

                    paper_data[short_cite]['short_cite'] = short_cite
                    paper_data[short_cite]['is_nn_paper'] = line_data['is_nn_paper']
                    paper_data[short_cite]['best'] = line_data['effectiveness']

    return  paper_data.values()


def parse_data_line(cols, idx_to_metric):
    
    name_match = re.search('\[(.+)\]', cols[0])
    short_cite = name_match.group(1)
    is_nn_paper = cols[2]

    effectiveness = {}
    for idx in range(3,len(cols)):
        metric = idx_to_metric[idx]
        try:
            sinle_effectiveness = float(cols[idx])
        except (IndexError, ValueError) as e :
            continue
        else:
            effectiveness[metric] = sinle_effectiveness

    line_data = {
        'short_cite': short_cite,
        'is_nn_paper': is_nn_paper,
        'effectiveness': effectiveness
    }

    return line_data

def write_new_md(new_md_file, paper_info):
    with open(new_md_file, 'w') as f:
        f.write('# Robust04 Effectiveness  \n\n') 

        f.write('| paper | is neural paper | baseline AP | best AP |  \n')
        f.write(':-------|-----------------|-------------|----------  \n')

        for single_paper_info in paper_info:
            try:
                f.write(
                    '| {} | {} | {} | {} |  \n'.format(
                                                    single_paper_info['short_cite'],
                                                    single_paper_info['is_nn_paper'],
                                                    single_paper_info['baseline']['AP'],
                                                    single_paper_info['best']['AP']
                                                )
                )

            except KeyError:
                # ignore paper not having AP
                pass

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--readme_file','-rf',default='README.md')
    parser.add_argument('--json_dest_file','-jf',default='robust04_paper_info.json')
    parser.add_argument('--new_md_file','-mf',default='robust04_paper_info.md')
    args=parser.parse_args()

    paper_info = get_paper_info(args.readme_file)
    with open(args.json_dest_file, 'w') as f:
        f.write(json.dumps(paper_info, indent=2))

    write_new_md(args.new_md_file, paper_info)

if __name__ == '__main__':
    main()
